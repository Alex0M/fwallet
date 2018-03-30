from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

from app import views

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'