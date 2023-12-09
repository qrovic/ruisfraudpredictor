import os
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)

current_dir = os.path.dirname(__file__)

# Construct the path to the model file
model_file_path = os.path.join(current_dir, "appdev2.pkl")

# Load model (Heroku's filesystem is read-only, so we'll use 'get' to safely access the environment variable)
with open(model_file_path, "rb") as file:
    model = pickle.load(file)

@flask_app.route("/")
def home():
    return render_template("index.html")

@flask_app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)

    prediction_name = 'Not Fraud' if prediction == 0 else 'Fraud'

    return render_template("index.html", prediction_text="The transaction is {}".format(prediction_name))

if __name__ == "__main__":
    # Use Heroku's provided port (or default to 5000 for local development)
    port = int(os.environ.get("PORT", 5000))
    # Run the app
    flask_app.run(host='0.0.0.0', port=port)
