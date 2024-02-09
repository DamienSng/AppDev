from wtforms import Form, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp

class CheckoutForm(Form):
    name = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired(), Email()])
    card_number = StringField('', validators=[DataRequired(), Length(min=16, max=16), Regexp(r'^\d{16}$')])
    exp_month = IntegerField('', validators=[DataRequired(), NumberRange(min=1, max=12, message="Invalid month")])
    exp_year = IntegerField('', validators=[DataRequired(), NumberRange(min=24, max=99, message="Invalid year")])  # Assuming a YY format, adjust min/max as needed
    cvv = StringField('', validators=[DataRequired(), Length(min=3, max=4), Regexp(r'^\d{3,4}$')])