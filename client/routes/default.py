from flask import render_template
from flask_login import current_user
from requests import get

from .. import app


@app.get("/")
def index():
    response = get(f"http://127.0.0.1:8000/post/get_all")
    posts = {
        "posts" : response.json()
    }
    print("*" * 80)
    print(posts)
    email = current_user.email
    nickname = email.split("@")[0]
    return render_template("index.html", nickname = nickname, **posts)