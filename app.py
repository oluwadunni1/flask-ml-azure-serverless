from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import traceback
import pandas as pd
import joblib
import sys 

# 1. Import your custom class
import preprocessing
from preprocessing import HousingFeatureEngineer

# 2. THE PATCH: Redirect __main__ to preprocessing
# This tells the model: "When you look for __main__.HousingFeatureEngineer, look here instead."
if 'HousingFeatureEngineer' not in sys.modules['__main__'].__dict__:
    sys.modules['__main__'].HousingFeatureEngineer = HousingFeatureEngineer

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    return "<h3>Custom Housing Price Prediction API (Active)</h3>"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Load the Pipeline
        model_pipeline = joblib.load("housing_full_pipeline.joblib")
        
        json_payload = request.json
        LOG.info("JSON payload: %s", json_payload)
        
        inference_payload = pd.DataFrame(json_payload)
        LOG.info("Inference payload DataFrame: %s", inference_payload)
        
        prediction = list(model_pipeline.predict(inference_payload))
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        LOG.error("Error during prediction: %s", str(e))
        LOG.error("Exception traceback: %s", traceback.format_exc())
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
