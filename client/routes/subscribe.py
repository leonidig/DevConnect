from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, select

from .. import app
from ..db import User, Session, Subscribe


def find_user_by_id(session, user_id):
    return session.scalar(select(User).where(User.id == user_id))


def is_already_subscribed(session, subscriber_id, subscribed_to_id):
    return session.scalar(
        select(Subscribe).where(
            Subscribe.subscriber_id == subscriber_id,
            Subscribe.subscribed_to_id == subscribed_to_id
        )
    )


@app.get("/subscribe/<int:subscribe_to_id>")
@login_required
def subscribe(subscribe_to_id: int):
    with Session.begin() as session:
        user_to_subscribe = find_user_by_id(session, subscribe_to_id)
        
        if not user_to_subscribe:
            return "User not found", 404

        if is_already_subscribed(session, current_user.id, subscribe_to_id):
            flash("You are already subscribed to this user.")
            return redirect(url_for("get_profile", username=user_to_subscribe.nickname))

        subscription = Subscribe(
            subscriber_id=current_user.id,
            subscribed_to_id=subscribe_to_id
        )
        current = find_user_by_id(session, current_user.id)
        user_to_subscribe.subscribers_count += 1
        current.subscribtions_count += 1
        session.add(subscription)
        flash("Subscribed successfully!")
        return redirect(url_for("get_profile", username=user_to_subscribe.nickname))


@app.post("/unsubscribe/<int:user_id>")
@login_required
def unsubscribe(user_id):
    with Session.begin() as session:
        user_to_unsubscribe = find_user_by_id(session, user_id)

        if not user_to_unsubscribe:
            return "User not found", 404

        subscription = is_already_subscribed(session, current_user.id, user_id)
        if not subscription:
            flash("You are not subscribed to this user.")
            return redirect(url_for("get_profile", username=user_to_unsubscribe.nickname))
        
        current = find_user_by_id(session, current_user.id)
        user_to_unsubscribe.subscribers_count -= 1
        current.subscribtions_count -= 1
        session.delete(subscription)
        flash("Unsubscribed successfully!")
        return redirect(url_for("get_profile", username=user_to_unsubscribe.nickname))

# @app.get("/subscribers/<string:username>")
# def get_user_subscribers(username: str):
#     with Session.begin() as session:
#         user = session.scalar(select(User).where(User.nickname == username))
#         if not user:
#             return {"error": "User not found"}, 404
#         subscriber_ids = session.scalars(select(Subscribe.subscriber_id).where(Subscribe.subscribed_to_id == user.id)).all()
#         subscribers = session.scalars(select(User.nickname).where(User.id.in_(subscriber_ids))).all()
#         print(subscribers)
#         return {"subscribers" : subscribers}