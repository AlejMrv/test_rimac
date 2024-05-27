from flask import Flask, request, jsonify
import time
import joblib
import pandas as pd
import json

# create a new Flask app
app = Flask(__name__)

# load the machine learning models
model_path = '/app/lightgbm_model.pkl'
model = joblib.load(model_path)

@app.route('/')
def hello_world():
    return "Model health"


@app.route('/predict', methods=["POST"])
def predictions():
    """
    Endpoint to get predictions. 
    ---
    parameters:
    -name: text
    in: query
    type: str 
    required: true
    """

    dataset_json = request.json
    dataset_dict = json.loads(dataset_json)
    df_dataset = pd.DataFrame.from_dict(dataset_dict)

    start_time = time.time()
    predictions = model.predict(X=df_dataset)

    return jsonify({"predictions": predictions.tolist(), "execution_time": time.time() - start_time})

# start the Flask app with gunicorn or uswgi
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)