#!/usr/bin/python
# Flask interface template and javascript retrieved from https://github.com/dongido001/flask_chatbot
from flask import Flask, request, jsonify, render_template
import os
import openai
import requests
import json
import time

app = Flask(__name__)
Setting = "The following is a text conversation of a user talking to a bot. The bot can assist user with academic related questions, such as: explaining technical Jargons."


class Timer:
    def start(self):
        self.start_time = time.time()

    def current_time(self):
        return time.time() - self.start_time


@app.route('/')
def index():
    return render_template('index.html')

openai.api_key = "YOUR API KEY"
def Complete_text(input_text):
    response = openai.Completion.create(

        model="text-curie-001",
        prompt=input_text,
        max_tokens=200,
        top_p=1,
        frequency_penalty= 0,
        presence_penalty= 0.6,
        temperature=0.9,

    )
    return response.choices[0].text.strip()


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    print('Sending message: {}'.format(message))
    timer = Timer()
    timer.start()
    fulfillment_text = Complete_text(Setting+"\n"+"User: "+message+"\nBot:")
    print(timer.current_time())
    print('Response: {}'.format(fulfillment_text))
    response_text = {"message": fulfillment_text}

    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
