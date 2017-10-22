from app import db
from datetime import datetime


class Pay(db.Model):

    __tablename__ = 'pay'

    amount = db.Column(db.Float)
    currency = db.Column(db.Integer)
    description = db.Column(db.String)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shop_invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer)

    def __init__(self, amount=None, currency=None, description=None, time_stamp=None, invoice_id=None):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.time_stamp = time_stamp
        self.invoice_id = invoice_id

    def __str__(self):
        return '<Description: %r>' % self.description
