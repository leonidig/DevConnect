from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import select, update

from ..db import Session, User, Subscribe

from .. import app


def get_subscribers_for_user(user_id: int):
    with Session.begin() as session:
        subscriber_ids = session.scalars(select(Subscribe.subscriber_id).where(Subscribe.subscribed_to_id == user_id)).all()
        subscribers = session.scalars(select(User.nickname).where(User.id.in_(subscriber_ids))).all()
        return subscribers
    

def get_subscriptions_for_user(user_id: int):
    with Session.begin() as session:
        subscriptions_ids = session.scalars(select(Subscribe.subscribed_to_id).where(Subscribe.subscriber_id == user_id)).all()
        subscriptions = session.scalars(select(User.nickname).where(User.id.in_(subscriptions_ids))).all()
        return subscriptions




@app.get("/profile/<string:username>")
def get_profile(username: str):
    with Session.begin() as session:
        user = session.scalars(select(User).where(User.nickname == username)).first()
        if not user:
            return "User not found"
        email = current_user.email
        current = email.split("@")[0]
        subscribers = get_subscribers_for_user(user.id)
        subscribtions = get_subscriptions_for_user(user.id)
        user_id = user.id
        print("*" * 80)
        print(subscribtions)
        return render_template("profile.html", user=user, current=current, subscribe_to_id=user_id, subscribtions=subscribtions, subscribers=subscribers)


@app.get("/edit_profile/<string:username>")
def get_edit(username: str):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.nickname == username))
        if not user:
            return "User not found", 404
        return render_template("edit_profile.html", user=user)


@app.post("/edit_profile/<string:username>")
def edit_data(username: str):
    email = current_user.email
    current = email.split("@")[0]

    with Session.begin() as session:
        selected_user = session.scalar(select(User).where(User.nickname == username))
        if not selected_user:
            return "User not found", 404
        if selected_user.nickname != current:
            return "Permission denied 403", 403  

        tech_stack = request.form.get("tech_stack")
        bio = request.form.get("bio")
        telegram_link = request.form.get("telegram_link")
        
        if telegram_link and not telegram_link.startswith("https://t.me/"):
            flash("Telegram link must be a valid link type (https://t.me/)")
            return redirect(url_for("get_edit", username=username))

        github_link = request.form.get("github_link")
        
        if github_link and not github_link.startswith("https://github.com/"):
            flash("GitHub link must be a valid link type (https://github.com/)")
            return redirect(url_for("get_edit", username=username))
        
        linkedin_link = request.form.get("linkedin_link")
        
        if linkedin_link and not linkedin_link.startswith("https://www.linkedin.com/in/"):
            flash("LinkedIn link must be a valid link type (https://www.linkedin.com/in/)")
            return redirect(url_for("get_edit", username=username))
        

        session.execute(
            update(User)
            .where(User.nickname == username)
            .values(
                tech_stack=tech_stack,
                bio=bio,
                telegram_link=telegram_link,
                github_link=github_link,
                linkedin_link=linkedin_link,
            )
        )
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



