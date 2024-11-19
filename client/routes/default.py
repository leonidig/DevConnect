from flask import render_template
from flask_login import current_user

from .. import app


@app.get("/")
def index():
    email = current_user.email
    nickname = email.split("@")[0]
    return render_template("index.html", nickname = nickname)