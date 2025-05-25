from os import getenv
from flask import Flask


app = Flask("client")
SECRET_KEY = getenv("SECRET_KEY")

from . import routes

app.config['SECRET_KEY'] = SECRET_KEY
