# ASL-Tutor

This repository is to be used as a learning aide for American Sign Language. This web application uses Angular for the front-end and Flask for the back-end

## Build images and run containers with Docker

Run `docker compose watch` which will start a web application that consists of an Angular front-end (default port `4200`) and a Flask back-end

## Access the application

In your browser navigate to `http://localhost:4200` (or whatever port you defined for the front-end in `docker-compose.yml`).

## Train model

In the flask-backend container, run `python ./model.py` to train the model. The model will save in the directory as `asl_model.keras`. Use `docker cp` to save the model to your host machine.

## Integrate model

Add `asl_model.keras` file to /backend

## Dataset

The dataset used for this project was not created by myself. It is available on Kaggle as the ASL Alphabet Dataset. https://www.kaggle.com/grassknoted/asl-alphabet