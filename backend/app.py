from flask import Flask,jsonify,request
import numpy as np
# import os
# import tensorflow as tf
# import tensorflow_datasets as tfds

app = Flask(__name__)

@app.route("/")
def home():
    return 'Hello Flask!!'

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)