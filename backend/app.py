import numpy as np
import json, requests
import tensorflow as tf
import os
import random
# import redis
import secrets
from io import BytesIO
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_cors import CORS
from asl_recognition_service import ASL_Recognition_Service

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True, origins=['https://localhost'], allow_headers=["Content-Type", "Authorization"])

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False        # Sessions expire when the browser is closed
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_NAME'] = 'session'

session_dir = '/app/sessions'

app.config['SESSION_FILE_DIR'] = session_dir

Session(app)




@app.route("/")
def home():
    return 'Welcome to Flask!'

@app.route('/hangman/start')
def start_game():
    word = "test"
    session['word'] = word
    session['masked_word'] = ["_"] * len(word)
    session["remaining_guesses"] = 7
    session["guessed_letters"] = []
    session["status"] = "in_progress"
    data = {"masked_word": session['masked_word'],
            "remaining_guesses": session['remaining_guesses'],
            "guessed_letters": session['guessed_letters'],
            "status": session['status']}
    return jsonify(data)

@app.route('/hangman/guess', methods=['POST'])
def guess():
    # Receives a guess from the front end
    data = request.get_json()
    if data:
        guessed_letter = data.get('guess').lower()

        # Extract game state from session
        word = session.get('word')
        masked_word = session.get('masked_word')
        remaining_guesses = session.get('remaining_guesses')
        guessed_letters = session.get('guessed_letters', [])
        status = session.get('status')

        # Validate if letter has already been guessed
        if guessed_letter in guessed_letters:
            return jsonify({'error': 'letter already guessed'}), 400
        guessed_letters.append(guessed_letter)

        # Check if guessed letter is in the word
        if guessed_letter in word:
            for i, letter in enumerate(word):
                if letter == guessed_letter:
                    masked_word[i] = guessed_letter
        else:
            remaining_guesses -= 1

        # Check for win/loss conditions
        if '_' not in masked_word:
            status = "won"
        elif remaining_guesses == 0:
            status = "lost"
        else:
            status = "in_progress"
        # Update the session with the game state

        session['masked_word'] = masked_word
        session['remaining_guesses'] = remaining_guesses
        session['guessed_letters'] = guessed_letters
        session['status'] = status


        # Return the updated game state to the front end (masked_word, remaining_guesses, guessed_letters, status)
        updated_game_data = {"masked_word": session['masked_word'],
            "remaining_guesses": session['remaining_guesses'],
            "guessed_letters": session['guessed_letters'],
            "status": session['status']}
        return jsonify(updated_game_data)
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/hangman/state')
def state():
    # Extract the current game state from the session (use session.get())
    word = session.get('word')
    masked_word = session.get('masked_word')
    remaining_guesses = session.get('remaining_guesses')
    guessed_letters = session.get('guessed_letters', [])
    status = session.get('status')

    if not word:
        return jsonify({'error': 'No active game found'}), 400

    # Check for win/loss conditions
    if '_' not in masked_word:
        status = "won"
    elif remaining_guesses == 0:
        status = "lost"
    else:
        status = "in_progress"

    # Send the game state to the front end
    updated_game_data = {"masked_word": masked_word,
            "remaining_guesses": remaining_guesses,
            "guessed_letters": guessed_letters,
            "status": status}
    return jsonify(updated_game_data)


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