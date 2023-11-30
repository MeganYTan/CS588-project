from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import io
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import json
import os
import openai

from openai import OpenAI
import requests

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)


# set up open ai
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key,
)

def send_system_command(command):
    """Function to send a system command to the OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model
            messages=[
                {"role": "system", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)


def get_completion(prompt, command = "", model="gpt-3.5-turbo", temperature = 0):
    if command != "" or command is not None:
        messages = [
            {"role": "system", "content": command},
            {"role": "user", "content": prompt}]
    else:
        messages = [
            {"role": "user", "content": prompt}]
    print(messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content



@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        df = pd.read_csv(file).drop(['name', 'version', 'package_name', 'bugs'], axis=1)
        total = calculate_defects(df)
        # get open api response
        training_data = get_training_data()
        response = get_completion(command=training_data.to_json() + "Use this data to train a model to predict the number of bugs. Use random forest regression",
                                  prompt="I want to predict the number of bugs based on these metrics. I don't want python code. Please give me a numerical response" + df.to_json())
        total_list = total.tolist()
        total_json = json.dumps(total_list)
        return jsonify({"total_defects": total_json, "open_AI_response": response})

@app.route('/', methods=['GET'])
def default():
    print('default route', flush=True)
    return '<h1>Hello world</h1>'

def calculate_defects(file):
    global model
    y_pred = model.predict(file)
    print (y_pred, flush = True)
    return y_pred

def get_training_data():
    return pd.read_csv('package_level_metrics_and_no_bugs.csv').iloc[0:30]
def train_model():
    model = RandomForestRegressor(random_state=32)
    package_metrics = get_training_data()
    # Assuming 'bug' is the target variable and all other relevant features are numeric
    X = package_metrics.drop(['name', 'version', 'package_name', 'bug'], axis=1)  # Drop non-numeric and target columns
    y = package_metrics['bug']

    # Preprocess the data (e.g., standardization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)
    model.fit(X, y)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    coefficient_of_dermination = r2_score(y_test, y_pred)
    rmse = mse ** 0.5

    # Print performance metrics
    print(f'Mean Squared Error: {mse}')
    print(f'R^2: {coefficient_of_dermination}')
    print(f'Ymin: {y.min()}, Ymax: {y.max()}')

    return model

# Train randomforestregressor
model = train_model()


if __name__ == '__main__':
    app.run(debug=True)
