from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("../models/obesity_model.pkl")

@app.route('/')

def home():
    return jsonify({
        "message": "Obesity Risk Classifier API Running"
    })

@app.route('/predict', methods=['POST'])

def predict():

    data = request.json

    features = np.array(data['features']).reshape(1, -1)

    prediction = model.predict(features)

    return jsonify({
        "prediction": int(prediction[0])
    })

if __name__ == "__main__":
    app.run(debug=True)