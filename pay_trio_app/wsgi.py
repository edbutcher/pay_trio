from whitenoise import WhiteNoise

from app.pay_trio_app.app import app

application = WhiteNoise(app)
