from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
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



    def is_active(self) -> bool:
        return True
    def is_authenticated(self) -> bool:
        return True
    def is_anonymous(self)->bool:
        return False
    def get_id(self)->str:
        return f"{self.id}"