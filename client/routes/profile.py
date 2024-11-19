from flask import render_template
from flask_login import current_user, login_required
from sqlalchemy import select

from ..db import Session, User

from .. import app


@app.get("/profile/<string:username>")
def get_profile(username: str):
    with Session.begin() as session:
        user = session.scalars(select(User).where(User.nickname == username)) 
        print('*' * 80)
        print(user)
        return user
    if not user:
        return "User not found"
    return render_template("profile.html", user = user)