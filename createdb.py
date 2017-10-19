from pay_trio_app import db
from pay_trio_app import models

db.create_all()
db.session.commit()
