from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from requests import post

from .. import app


@app.get("/create_post")
@login_required
def create():
    return render_template("create.html")



@app.post("/create_post")
@login_required
def create_post():
    data = {
        "title" : request.form.get("title"),
        "content" : request.form.get("content"),
        "author" : current_user.email,
        "timestamp" : datetime.now().isoformat()
    }
    print("*" * 80)
    print(data)
    response = post("http://127.0.0.1:8000/post/create", json=data)
    if response.status_code == 201:
        return redirect(url_for("index"))
    else:
        return "Error"