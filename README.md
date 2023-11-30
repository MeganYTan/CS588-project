# CS588-project

This is the repository for CS588 Project

The purpose of this project is to compare the results of defect prediction between a model trained using RandomForestRegressor and OpenAI's API response.

## Answers

1. How many total lines of code written (rough estimates are acceptable)?

About 350 lines of code.

2. What are the features implemented and functional in your project?

Features implemented for front-end and backend

- React Frontend with the ability to upload a csv folder of a single lines of software metrics

- React Frontend that calls a Flask API, and shows the results

- Flask API to take in a csv folder

- Trained RandomForestRegressor used to predict the number of bugs based on the metrics

- Functionality to call OpenAI's API with a set prompt to predict the number of bugs based on the inputed csv and training data, by converting the csv to json format

Features implemented for experiment:

- Trained RandomForestRegressor model used to predict the number of bugs based on software metrics

- Use the RandomForestRegressor model to predict the number of bugs for 135 lines of test data

- Call OpenAI's API to predict the number of bugs for the same 135 lines of test data

- Results reported, analyzed, and visualized

## Project Structure

PSOWE Dataset - This is the raw data collected. It is collected into a single csv file in project/defect_prediction_flask

<br/><br/>
project folder - contains the code for the project, which consist of a flask server and a react frontend.

&nbsp; defect-prediction-flask subfolder - contains csv files, which is a summary of the files collected for the project, as well as bug_prediction_<number> files, which are single vector files used with the UI to demonstrate the project. 

&nbsp; &nbsp; app.py contains the flask code for the server

<br/>
&nbsp; defect-prediction-ui subfolder - contains code for the react frontend. CSVUploader component is the main component to upload the csv files

<br/>
Experiment Script.ipnyb - contains the experiment script to run the experiment. The data and results are stored in experiment_data_and_results subfolder. The data used is a randomly selected subset of the original dataset minus the training dataset. Due to OpenAI's API token and rate limits, only 135 rows of data are used for the experiment. 


## To run the project

cd project/defect-prediction-flask

pip -r requirements.txt

set OPEN_AI_APIKEY = <your api key>

python app.py

cd ../defect-prediction-ui

npm install

npm start
