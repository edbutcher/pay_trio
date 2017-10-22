from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import models


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')  # DeveloperConfig and ProductionConfig


db = SQLAlchemy(app)
db.create_all()
db.session.commit()
