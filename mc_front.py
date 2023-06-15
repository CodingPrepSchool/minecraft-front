from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import json
import requests
from forms import PostForm, TipForm

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'



baseURL = 'http://127.0.0.1:8080/'


@app.route("/error", methods=["GET"])
def error():
  return render_template("error.html")

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
      else:
           print('response', response)
           return redirect("/error")
      
@app.route("/deletepost", methods=["GET"])
def removes_post():
    post_id = request.args.get('id')
    uri = baseURL + 'api/post/' + post_id
    try: 
      response = requests.delete(uri)
    except requests.ConnectionError:
      return "Connection Error"
    if response.status_code == 200:
      return redirect("/")
    else:
      return redirect("/error")


@app.route("/survivaltips", methods=["GET"])
def tips():
  tip_form = TipForm(csrf_enabled=False)
  uri = baseURL + 'api/tips' 
  try: 
    response = requests.get(uri)
  except requests.ConnectionError:
    return "Connection Error"
  json_response = response.text
  data = json.loads(json_response)
  return render_template("survival_tips.html", tips=data, template_form=tip_form)

@app.route("/deletetip", methods=["GET"])
def removes_tip():
    tip_id = request.args.get('id')
    uri = baseURL + 'api/tips/' + tip_id
    try: 
      response = requests.delete(uri)
    except requests.ConnectionError:
      return "Connection Error"
    if response.status_code == 200:
      return redirect("/")
    else:
      return redirect("/error")
    
@app.route("/post_tip", methods=["POST"])
def create_tip():
  tip_form = TipForm(csrf_enabled=False)
  uri = baseURL + 'api/tips'
  if tip_form.validate_on_submit():
      tip_json = {
        "tip": tip_form.tip.data,
        "description": tip_form.description.data,
      }
      try: 
        response = requests.post(uri, json = tip_json)
      except requests.ConnectionError:
        return "Connection Error"
      if response.status_code == 201:
        return redirect("/survivaltips")
      else:
           print('response', response)
           return redirect("/error")
      
@app.route("/edit_tip", methods=["GET"])
def tip_recipe():
  tip_id = request.args.get('id')
  uri = baseURL + '/api/tips/edit' + tip_id
  try: 
    response = requests.get(uri)
  except requests.ConnectionError:
    return "Connection Error"
  json_response = response.text
  data = json.loads(json_response)
  "tip": tip_form.tip.data
  "description": tip_form.description.data

  form_values = {
    "id": tip_id,
    "tip": data["tip"],
    "description": data["description"]
  }

  tip_form = TipForm(csrf_enabled=False, data=form_values)
  return render_template("edit_tip.html", template_form=tip_form)


@app.route("/edit_tip", methods=["POST"])
def edit_tip_post():
  tip_form = TipForm(csrf_enabled=False)
  id = tip_form.id.data
  uri = baseURL + '/api/tips/edit' + id
  if tip_form.validate_on_submit():
      tip_json = {
        "tip": tip_form.tip.data,
        "description": tip_form.description.data,
      }
      try: 
        response = requests.put(uri, json = tip_json)
      except requests.ConnectionError:
        return "Connection Error"
      if response.status_code == 201:
        return redirect("/browse_recipes")
      else:
        return redirect("/error")