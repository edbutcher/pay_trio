from whitenoise import WhiteNoise

from app import app

application = WhiteNoise(app)
