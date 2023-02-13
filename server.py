from flask import Flask, request, render_template, jsonify, session
from db import setup
import os
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']
setup()


@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route('/hi', methods=['GET'])
def hello():
  user_name = request.args.get("userName", "unknown")
  return render_template('hello.html', user=user_name) 

@app.route('/devito', methods=['GET'])
def Danny_Devito():
	user_name = request.args.get("userName", "unknown")
	return render_template('devito.html', user=user_name) 

@app.route('/survey', methods=['GET'])
def survey():
	return render_template('question.html')

@app.route('/results', methods=['POST'])
def results():
	data = request.form
	answer = data['didHeWin']
	temp = (answer == "yes")
	return render_template('results.html', survey_answer=answer, correct=temp) 

@app.route('/api/fact', methods=['GET'])
def get_random_fact():
	return jsonify({"id":17, "source": "my brain", "fact": "I love mcdonalds"})

@app.route('/api/fact', methods=['POST'])
def take_in_fact():
	print(request.json)
	return jsonify({"response": "okay, good fact"})