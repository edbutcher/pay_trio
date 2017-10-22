from whitenoise import WhiteNoise

from pay_trio_app.app import app

application = WhiteNoise(app)
