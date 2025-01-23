# Machine Downtime Prediction API

## Description

This Flask API predicts the likelihood of machine downtime. It uses a Logistic Regression model trained on a dataset of historical machine data. The API allows you to upload a CSV file for training the model, and then use the trained model to predict downtime for new data points.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Harshadeep6/Machine-Downtime.git
    cd Machine-Downtime
    ```
2. **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    ```
3. **Activate the virtual environment:**

    *   On Windows:

        ```bash
        venv\Scripts\activate
        ```

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```
4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Upload Data

*   **Endpoint:** `/upload`
*   **Method:** `POST`
*   **Request:**
    *   Form-data with a file named `data` (the CSV file containing training data). The CSV file should have a 'Downtime' column indicating downtime (0 for yes, 1 for no) and other columns that are specified in the 'featuresList' variable in the 'train_model' function.
*   **Response:**
    *   `"File uploaded and saved successfully!"` if successful.
    *   Error message if no file is selected or if there's an issue.

### 2. Train Model

*   **Endpoint:** `/train`
*   **Method:** `POST`
*   **Request:**
    *   Make sure a file named `data.csv` is present in the `uploads` folder.
*   **Response:**

    ```json
    {
        "Accuracy": 0.81,
        "F1 Score": 0.81
    }
    ```

    *   `Accuracy` and `F1 Score` represent the model's performance on the test set.

### 3. Predict Downtime

*   **Endpoint:** `/predict`
*   **Method:** `POST`
*   **Request:**

    ```json
    {
        "Hydraulic_Pressure(bar)": 90.43,
        "Coolant_Pressure(bar)": 6.863944117,
        "Air_System_Pressure(bar)": 6.833893108,
        "Coolant_Temperature": 17.1,
        "Hydraulic_Oil_Temperature(?C)": 39.4,
        "Spindle_Bearing_Temperature(?C)": 34.3,
        "Spindle_Vibration(?m)": 0.818,
        "Tool_Vibration(?m)": 23.104,
        "Spindle_Speed(RPM)": 17919,
        "Voltage(volts)": 313,
        "Torque(Nm)": 16.44955444,
        "Cutting(kN)": 2.26
    }
    ```

    *   The JSON payload should contain the features used during training. These features are present in the `featuresList` variable in the `train_model` function.
*   **Response:**

    ```json
    {
        "Confidence": 0.81,
        "Downtime": "Yes"
    }
    ```

    or

    ```json
    {
        "Downtime": "No",
        "Confidence": 0.85
    }
    ```

    *   `Downtime`: "Yes" or "No" indicating the prediction.
    *   `Confidence`: The accuracy score of the trained model.

### Running the API

1. **Start the Flask development server:**

    ```bash
    python app.py
    ```
2. **The API will be accessible at:** `http://127.0.0.1:5000/`

## Features

*   **Upload Data:** Upload a CSV file for training.
*   **Train Model:** Train a Logistic Regression model on the uploaded data.
*   **Predict Downtime:** Get downtime predictions for new data.
*   **Model Evaluation:** Provides Accuracy and F1 Score to assess model performance.
*   **Error Handling:** Returns informative messages for missing files or incorrect input.
*   **Organized File Structure:** Stores uploaded data in the `uploads` directory and the trained model in the `model` directory.

## Notes

*   The model's performance depends heavily on the quality and relevance of the training data. Assuming that you provide good preprocessed data (i.e without any NULL values, etc.)
*   The `featuresList` variable within the `/train` route determines which columns from the CSV are used for training. Make sure these features are present in your uploaded data.
*   The model is saved as `LogisticRegressionModel.joblib` in the `model` directory after training.
