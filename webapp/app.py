from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import traceback
import pandas as pd
import joblib
import sys 
import os 
# ---------------------------------------------------------
# 1. SETUP & CUSTOM CLASS HANDLING
# ---------------------------------------------------------
import preprocessing  # pylint: disable=unused-import
from preprocessing import HousingFeatureEngineer

if 'HousingFeatureEngineer' not in sys.modules['__main__'].__dict__:
    sys.modules['__main__'].HousingFeatureEngineer = HousingFeatureEngineer

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# ---------------------------------------------------------
# 2. GLOBAL MODEL LOADING
# ---------------------------------------------------------
MODEL_PATH = "housing_full_pipeline.joblib"
model_pipeline = None

try:
    LOG.info(f"Loading model from {MODEL_PATH}...")
    model_pipeline = joblib.load(MODEL_PATH)
    LOG.info("Model loaded successfully!")
except Exception as e:
    LOG.error(f"CRITICAL ERROR: Failed to load model: {e}")
    LOG.error(traceback.format_exc())

# ---------------------------------------------------------
# 3. ENDPOINTS
# ---------------------------------------------------------
@app.route("/")
def home():
    status = "Active" if model_pipeline else "Error: Model not loaded"
    return f"<h3>Simple House Price Prediction API ({status})</h3>"

@app.route("/metadata", methods=["GET"])
def metadata():
    """
    Returns info about the model for auditing.
    """
    return jsonify({
        "name": "Simple House Price Predictor",
        "version": "v1.0.0",
        "author": "Dunni",
        "description": "Predicts house value based on basic real estate features.",
        "input_schema": [
            "SquareFeet", "Bedrooms", "Bathrooms", "YearBuilt", "Neighborhood"
        ]
    })

@app.route("/predict", methods=["POST", "GET"])
def predict():
    # ---------------------------------------------------------
    # EXERCISE REQUIREMENT: Handle GET requests with CORRECT examples
    # ---------------------------------------------------------
    if request.method == "GET":
        return jsonify({
            "message": "Send a POST request to this endpoint with the following JSON structure:",
            "example_payload": {
                "SquareFeet": [2500],
                "Bedrooms": [3],
                "Bathrooms": [2],
                "YearBuilt": [2015],
                "Neighborhood": ["Rural"]
            }
        })

    # ---------------------------------------------------------
    # EXISTING LOGIC: Handle POST requests (Inference)
    # ---------------------------------------------------------
    if not model_pipeline:
        return jsonify({"error": "Model is not loaded on the server."}), 500

    try:
        json_payload = request.json
        LOG.info(f"Received request with {len(json_payload)} keys")
        
        # Convert JSON to DataFrame
        inference_payload = pd.DataFrame(json_payload)
        
        # Predict
        prediction = list(model_pipeline.predict(inference_payload))
        
        LOG.info(f"Prediction generated: {prediction}")
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        LOG.error(f"Error during prediction: {str(e)}")
        LOG.error(traceback.format_exc())
        return jsonify({"error": str(e), "message": "Check inputs against schema."})

if __name__ == "__main__":
    # Get the PORT from the Operating System (Azure/AWS), 
    # or use 5000 if running locally.
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host="0.0.0.0", port=port, debug=True)