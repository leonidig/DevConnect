from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from .. import Base

class User(Base):
    __tablename__ = 'users'
    
    nickname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    registration_date: Mapped[datetime]
    tech_stack: Mapped[str]
    bio: Mapped[str] 
    telegram_link: Mapped[str]
    github_link: Mapped[str]
    linkedin_link: Mapped[str]


    subscriptions: Mapped[list["Subscribe"]] = relationship(
        "Subscribe", 
        back_populates="subscriber", 
        cascade="all, delete-orphan",
        foreign_keys="Subscribe.subscriber_id"  
    )
    

    subscribers: Mapped[list["Subscribe"]] = relationship(
        "Subscribe", 
        back_populates="subscribed_to", 
        cascade="all, delete-orphan",
        foreign_keys="Subscribe.subscribed_to_id" 
    )

    def is_active(self) -> bool:
        return True

    def is_authenticated(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return f"{self.id}"
    

class Subscribe(Base):
    __tablename__ = "subscriptions"

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subscribed_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    subscriber: Mapped["User"] = relationship(
        "User", 
        foreign_keys=[subscriber_id], 
        back_populates="subscriptions"
    )
    subscribed_to: Mapped["User"] = relationship(
        "User", 
        foreign_keys=[subscribed_to_id], 
        back_populates="subscribers"
    )
