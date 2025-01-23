from flask import Flask, request, jsonify
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import joblib

# Creating the Flask app
app = Flask(__name__)

# The uploaded csv file will be stored in the 'uploads' folder
if not os.path.exists('uploads'):
    os.mkdir('uploads')
# The trained model will be saved in the 'model' folder
if not os.path.exists('model'):
    os.mkdir('model')

# Creating the 'upload' route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'data' not in request.files:
        return 'No file part'
    file = request.files['data']
    if file.filename == '':
        return ' No selected file'
    if file:
        file.save(os.path.join('uploads', file.filename))
        return 'File uploaded and saved successfully!'


finalFeatures = [] # The final features which will be used for model training
# Creating the 'train' route
@app.route('/train', methods=['POST'])
def train_model():

    featuresList = ['Hydraulic_Pressure(bar)', 'Coolant_Pressure(bar)', 'Air_System_Pressure(bar)', 'Coolant_Temperature', 'Hydraulic_Oil_Temperature(?C)', 'Spindle_Bearing_Temperature(?C)', 'Spindle_Vibration(?m)', 'Tool_Vibration(?m)', 'Spindle_Speed(RPM)', 'Voltage(volts)', 'Torque(Nm)', 'Cutting(kN)']

    # Loading the uploaded dataset for model training
    dataset = pd.read_csv(os.path.join('uploads', 'data.csv'))
    target = dataset['Downtime']

    # Getting the required features for model training
    for feature in list(dataset.columns):
        if feature in featuresList:
            finalFeatures.append(feature)
            
    # Splitting the data
    X_train, X_test, Y_train, Y_test = train_test_split(dataset[finalFeatures], target, test_size=0.2, random_state=42)

    # Training the model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # Saving the model
    joblib.dump(model, os.path.join('model', 'LogisticRegressionModel.joblib'))

    # Testing the model on the test set
    Y_pred = model.predict(X_test)

    # Calculating the Accuracy Score and the F1 Score
    app.config['ACCURACY'] = accuracy_score(Y_test, Y_pred)
    app.config['F1_SCORE'] = f1_score(Y_test, Y_pred)

    return jsonify({"Accuracy": round(app.config['ACCURACY'], 2), "F1 Score": round(app.config['F1_SCORE'], 2)})


# Creating the 'predict' route
@app.route('/predict', methods=['POST'])
def predict_downtime():

    # Getting the prediction input
    data = request.get_json()
    data = pd.DataFrame(data, index=[0])

    # Loading the trained model
    model = joblib.load(os.path.join('model', 'LogisticRegressionModel.joblib'))

    # Predicting the downtime
    prediction = model.predict(data)

    # Sending the JSON response
    if prediction == 0:
        return jsonify({"Downtime": "Yes", "Confidence": round(app.config['ACCURACY'], 2)})
    
    return jsonify({"Downtime": "No", "Confidence": round(app.config['ACCURACY'], 2)})

if __name__ == '__main__':
    app.run(debug=True)