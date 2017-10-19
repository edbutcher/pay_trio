from flask import render_template, request
from pay_trio_app import app
from pay_trio_app.forms import PayForm

import random
import hashlib
import json
import requests

# Add secret "key" from store.

shop_id = '305100'  # Shop id from store


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PayForm()

    if request.method == 'POST' and form.validate_on_submit():

        amount = str(form.amount.data)
        currency = form.currency.data
        description = form.description.data
        shop_invoice_id = str(random.randrange(1000, 10001, 1))

        if currency == '840':
            """USD logic with TIP."""

            # Generate md5 hex
            pre_sign = bytes(":".join([amount, currency, shop_id]) + key, 'utf-8')
            sign = hashlib.md5(pre_sign).hexdigest()

            context = {
                "amount": amount,
                "currency": currency,
                "shop_id": shop_id,
                "sign": sign,
                "shop_invoice_id": shop_invoice_id,
                "description": description,
            }

            # Request to Tip
            url = 'https://tip.pay-trio.com/ru/'
            tip_response = requests.post(url, params=context)
            context = tip_response.text

            # Add answer from Tip request and save to db.

            return render_template('type_tip.html', context=context)

        elif currency == '978':
            """EUR logic with Invoice request"""

            payway = 'payeer_eur'

            # Generate md5 hex
            pre_sign = bytes(":".join([amount, currency, payway, shop_id]) + key, 'utf-8')
            sign = hashlib.md5(pre_sign).hexdigest()

            context = {
                "amount": amount,
                "currency": currency,
                "payway": payway,
                "shop_id": shop_id,
                "sign": sign,
                "shop_invoice_id": shop_invoice_id,
                "description": description,
            }

            context = json.dumps(context, separators=(',', ':'))

            # Request to Invoice
            url = 'https://central.pay-trio.com/invoice'
            headers = {'Content-Type': 'application/json'}
            invoice_response = requests.post(url, headers=headers,  data=context)
            context = invoice_response.text

            # Add answer from Invoice request and save to db.

            return render_template('type_invoice.html', context=context)

    return render_template('home.html', form=form)




