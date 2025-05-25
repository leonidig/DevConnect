from sqlalchemy.orm import Mapped, DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy import create_engine


ENGINE = create_engine("sqlite:///posts.db", echo = True)
Session = sessionmaker(bind = ENGINE)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key = True)


def up():
    Base.metadata.create_all(ENGINE)


def down():
    Base.metadata.drop_all(ENGINE)


def migrate():
    up()
    down()


def get_session():
    with Session.begin() as session:
        yield session


from .models import Post

up()