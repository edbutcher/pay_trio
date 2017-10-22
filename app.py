from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, FloatField
from wtforms.validators import NumberRange, InputRequired


from datetime import datetime
import random
import hashlib
import json
import requests
import os


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')  # DeveloperConfig and ProductionConfig

db = SQLAlchemy(app)


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


db.create_all()
db.session.commit()


class PayForm(FlaskForm):
    """Pay form."""
    amount = FloatField('Amount', validators=[InputRequired(),
                                                NumberRange(min=0.00, message="Must be a number biggest than 0.00")])
    currency = SelectField('Currency', choices=[('840', 'USD'), ('978', 'EUR')])
    description = TextAreaField('Description', validators=[InputRequired()])


key = os.environ['my_key']

shop_id = '305100'  # Shop id from store


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PayForm()

    if request.method == 'POST' and form.validate_on_submit():

        amount = str(form.amount.data)
        currency = form.currency.data
        description = form.description.data
        shop_invoice_id = str(random.randrange(1000, 10001, 1))  # For real project better use UUID

        if currency == '840':
            """
            USD logic with TIP.
            Required parameters: amount, currency, shop_id, shop_invoice_id, sign.
            """

            # Generate md5 hex
            sign = hashlib.md5((":".join([amount, currency, shop_id, shop_invoice_id]) + key).encode('utf-8')).hexdigest()

            context = {
                "amount": amount,
                "currency": currency,
                "shop_id": shop_id,
                "sign": sign,
                "shop_invoice_id": shop_invoice_id,
                "description": description,
            }

            instance = Pay()
            instance.amount = float(amount)
            instance.currency = int(currency)
            instance.description = description
            instance.shop_invoice_id = int(shop_invoice_id)
            instance.invoice_id = None

            db.session.add(instance)
            db.session.commit()

            return render_template('type_tip.html', context=context)  # In template hidden some params from user.

        elif currency == '978':
            """
            EUR logic with Invoice request.
            Required parameters: amount, currency, payway, shop_id, shop_invoice_id, sign.
            """

            payway = 'payeer_eur'

            # Generate md5 hex
            sign = hashlib.md5((":".join([amount, currency, payway, shop_id, shop_invoice_id]) + key).encode('utf-8')).hexdigest()

            context = {
                "description": description,
                "payway": payway,
                "shop_invoice_id": shop_invoice_id,
                "sign": sign,
                "currency": currency,
                "amount": amount,
                "shop_id": shop_id,
            }

            context = json.dumps(context, separators=(',', ':'))

            # Request to Invoice
            url = 'https://central.pay-trio.com/invoice'
            headers = {'Content-Type': 'application/json'}
            invoice_response = requests.post(url, headers=headers,  data=context)
            data = invoice_response.json()

            if invoice_response.status_code == requests.codes.ok and data['result'] == 'ok':

                data_method = data['data']['method']
                data_source = data['data']['source']
                data_invoice_id = data['data']['invoice_id']

                data_m_curorderid = data['data']['data']['m_curorderid']
                data_m_historytm = data['data']['data']['m_historytm']
                data_m_historyid = data['data']['data']['m_historyid']
                data_lang = data['data']['data']['lang']

                context = {

                    "method": data_method,
                    "source": data_source,
                    "m_curorderid": data_m_curorderid,
                    "m_historytm": data_m_historytm,
                    "m_historyid": data_m_historyid,
                    "lang": data_lang,
                }

                instance = Pay()
                instance.amount = float(amount)
                instance.currency = int(currency)
                instance.description = description
                instance.shop_invoice_id = int(shop_invoice_id)
                instance.invoice_id = int(data_invoice_id)

                db.session.add(instance)
                db.session.commit()

                return render_template('type_invoice.html', context=context)

            else:

                error = data['message']
                return render_template('error.html', context=error)

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run()
