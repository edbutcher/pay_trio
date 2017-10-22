from whitenoise import WhiteNoise

from pay_trio_app import app

application = WhiteNoise(app)