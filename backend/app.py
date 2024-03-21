import numpy as np
import json, requests
import tensorflow as tf
import os
import random
from io import BytesIO
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify
from flask_cors import CORS
from asl_recognition_service import ASL_Recognition_Service

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():

    return 'Welcome to Flask!'

@app.route('/predict', methods=['POST'])
def predict():

    # get image from client and save it
    image = request.files["file"]
    if image.filename == '':
      return jsonify('No selected file')
    file_name = 'snapshot.jpeg'
    image.save(file_name)

    # invoke sign language recognition service
    asl = ASL_Recognition_Service()

    # make a prediction
    predicted_letter = asl.predict(file_name)

    # remove the image
    # os.remove(file_name)

    # send back the predicted letter in json format
    data = {"letter": predicted_letter}
    return jsonify(data)


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)