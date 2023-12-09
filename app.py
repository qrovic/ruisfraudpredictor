import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("appdev2.pkl", "rb"))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)

    prediction_name=''
    if prediction == 0:
        prediction_name='Not Fraud'
    else:
        prediction_name='Fraud'

    return render_template("index.html", prediction_text = "The transaction is {}".format(prediction_name))

if __name__ == "__main__":
    flask_app.run(debug=True)