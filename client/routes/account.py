from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import select, update

from ..db import Session, User

from .. import app


@app.get("/profile/<string:username>")
def get_profile(username: str):
    with Session() as session:
        user = session.scalars(select(User).where(User.nickname == username)).first()
        if not user:
            return "User not found"
        email = current_user.email
        current = email.split("@")[0]
        return render_template("profile.html", user=user, current=current)



@app.get("/edit_profile/<string:username>")
def get_edit(username: str):
    return render_template("edit_profile.html", username=username)


@app.post("/edit_profile/<string:username>")
def edit_data(username: str):
    email = current_user.email
    current = email.split("@")[0]

    with Session.begin() as session:
        selected_user = session.scalar(select(User).where(User.nickname == username))

        if selected_user.nickname != current:
            return "Permission denied 403", 403  
        
        tech_stack = request.form.get("tech_stack")
        bio = request.form.get("bio") 
        telegram_link = request.form.get("telegram_link")
        github_link = request.form.get("github_link")
        linkedin_link = request.form.get("linkedin_link")

        upd = update(User).where(User.nickname == username).values(
            tech_stack=tech_stack,
            bio=bio,
            telegram_link=telegram_link,
            github_link=github_link,
            linkedin_link=linkedin_link
        )
        session.execute(upd)
        return redirect(url_for("index"))



@app.get('/search')
def search_user():
    query = request.args.get("query", '')
    if query:
        with Session.begin() as session:
            target = session.scalars(select(User).filter(User.nickname.ilike(f'%{query}%'))).all()
            print("Users found:", [user.nickname for user in target])
            return render_template("users.html", query=query, users=target)
    return render_template("index.html", query=query, users=[])
