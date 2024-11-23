from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select

from .. import app
from ..db import User, Session, Subscribe


@app.get("/subscribe/<int:subscribe_to_id>")
@login_required 
def subscribe(subscribe_to_id: int):
    with Session.begin() as session:  
        user_to_subscribe = session.scalars(select(User).where(User.id == subscribe_to_id)).first()
        current = session.scalar(select(User).where(User.email == current_user.email))
        

        if not user_to_subscribe:
            return "User not found", 404
        

        existing_subscription = session.query(Subscribe).filter_by(
            subscriber_id=current_user.id,
            subscribed_to_id=user_to_subscribe.id
        ).first()

        if existing_subscription:
            flash("You are already subscribed to this user.")
            return redirect(url_for("get_profile", username=user_to_subscribe.nickname))
        print("*" * 80)
        print(current_user.id)
        subscription = Subscribe(
            subscriber_id=current_user.id,
            subscribed_to_id=user_to_subscribe.id
        )
        user_to_subscribe.subscribers_count += 1
        current.subscribtions_count += 1
        session.add(subscription) 


        flash("Subscribed successfully!")
        return redirect(url_for("get_profile", username=user_to_subscribe.nickname))
