from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, FloatField
from wtforms.validators import NumberRange, InputRequired


class PayForm(FlaskForm):
    """Pay form."""
    amount = FloatField('Amount', validators=[InputRequired(),
                                                NumberRange(min=0.00, message="Must be a number biggest than 0.00")])
    currency = SelectField('Currency', choices=[('840', 'USD'), ('978', 'EUR')])
    description = TextAreaField('Description', validators=[InputRequired()])
