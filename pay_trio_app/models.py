from pay_trio_app import db
from datetime import datetime


class Pay(db.Model):

    __tablename__ = 'pay'

    amount = db.Column(db.Integer)
    currency = db.Column(db.String)
    description = db.Column(db.String)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shop_invoice_id = db.Column(db.String, primary_key=True)

    def __init__(self, amount=None, currency=None, description=None, time_stamp=None):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.time_stamp = time_stamp

    def __str__(self):
        return '<Description: %r>' % self.description
