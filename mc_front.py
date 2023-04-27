from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import json
import requests

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'



baseURL = 'http://127.0.0.1:8080/'

@app.route("/", methods=["GET"])
def homepage():
    uri = baseURL + 'api/posts'
    try: 
      response = requests.get(uri)
    except requests.ConnectionError:
      return "Connection Error"
    json_response = response.text
    data = json.loads(json_response)
    return render_template("homepage.html")