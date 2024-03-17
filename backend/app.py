import numpy as np
import json, requests
import tensorflow as tf
from io import BytesIO
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
class_names = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z']

@app.route("/")
def home():

    return 'Welcome to Flask!'

@app.route('/predict', methods=['POST'])
def predict():

    return jsonify('Success')



if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)