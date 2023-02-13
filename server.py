from flask import Flask, request, render_template, jsonify, session, url_for, redirect
from db import setup
from os import environ as env
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = env['FLASK_SECRET']
setup()

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENTID"),
    client_secret=env.get("AUTH0_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
)

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

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