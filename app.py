from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import traceback
import pandas as pd
import joblib  # FIXED: Modern import
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""
    LOG.info("Scaling Payload: %s", payload) # FIXED: Logging format
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    html = "<h3>Sklearn Prediction Home: From Azure Pipelines (Continuous Delivery)</h3>"
    return html

@app.route("/predict", methods=["POST"])
def predict():
    """Performs an sklearn prediction"""
    
    # 1. Load Model
    try:
        clf = joblib.load("boston_housing_prediction.joblib")
    except Exception as e:
        LOG.error("Error loading model: %s", str(e))
        LOG.error("Exception traceback: %s", traceback.format_exc())
        return "Model not loaded"

    # 2. Process Data
    # FIXED: The code below is now reachable (fixed indentation)
    try:
        json_payload = request.json
        LOG.info("JSON payload: %s", json_payload) # FIXED: Logging format
        
        inference_payload = pd.DataFrame(json_payload)
        LOG.info("inference payload DataFrame: %s", inference_payload) # FIXED: Logging format
        
        scaled_payload = scale(inference_payload)
        prediction = list(clf.predict(scaled_payload))
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        LOG.error("Error during prediction: %s", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # It is safer to use port 5000 locally, but ensure Azure knows about it.
    app.run(host="0.0.0.0", port=5000, debug=True)