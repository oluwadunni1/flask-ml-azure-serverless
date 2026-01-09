from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import traceback
import pandas as pd
import joblib

# 1. CRITICAL IMPORT: This allows joblib to understand your custom pipeline
from preprocessing import HousingFeatureEngineer

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    html = "<h3>Custom Housing Price Prediction API (Active)</h3>"
    return html

@app.route("/predict", methods=["POST"])
def predict():
    """Performs a prediction using the custom pipeline"""
    
    # 2. Load the Pipeline (Model + Preprocessing)
    try:
        # This file contains the "Mega Pipeline" that does scaling -> engineering -> prediction
        model_pipeline = joblib.load("housing_full_pipeline.joblib")
    except Exception as e:
        LOG.error("Error loading model: %s", str(e))
        LOG.error("Exception traceback: %s", traceback.format_exc())
        return "Model not loaded"

    try:
        # 3. Get Data
        json_payload = request.json
        LOG.info("JSON payload: %s", json_payload)
        
        inference_payload = pd.DataFrame(json_payload)
        LOG.info("Inference payload DataFrame: %s", inference_payload)
        
        # 4. Predict
        # We do NOT need to call a separate scale() function. 
        # The pipeline handles raw data automatically.
        prediction = list(model_pipeline.predict(inference_payload))
        
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        LOG.error("Error during prediction: %s", str(e))
        LOG.error("Exception traceback: %s", traceback.format_exc())
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
