from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from pay_trio_app import views


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')  # DeveloperConfig and ProductionConfig

db = SQLAlchemy(app)

from pay_trio_app.models import Pay

db.create_all()
db.session.commit()


if __name__ == '__main__':
    app.run()
