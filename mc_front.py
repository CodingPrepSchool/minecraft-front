from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import json
import requests
from forms import PostForm

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'



baseURL = 'http://127.0.0.1:8080/'

@app.route("/", methods=["GET"])
def homepage():
    post_form = PostForm(csrf_enabled=False)
    uri = baseURL + 'api/posts'
    try: 
      response = requests.get(uri)
    except requests.ConnectionError:
      return "Connection Error"
    json_response = response.text
    data = json.loads(json_response)
    return render_template("homepage.html",  rows=data, template_form=post_form)


@app.route("/post", methods=["POST"])
def create_post():
  post_form = PostForm(csrf_enabled=False)
  uri = baseURL + 'api/post'
  if post_form.validate_on_submit():
      post_json = {
        "post": post_form.post.data,
      }
      try: 
        response = requests.post(uri, json = post_json)
      except requests.ConnectionError:
        return "Connection Error"
      if response.status_code == 201:
        return redirect("/")