from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object('config.DevelopConfig')  # DeveloperConfig and ProductionConfig


db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

import pay_trio_app.views


