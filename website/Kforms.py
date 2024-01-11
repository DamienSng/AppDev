from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, SubmitField, widgets
from wtforms.validators import ValidationError


class UserPreferencesForm(FlaskForm):
    top_preferences = SelectMultipleField('Top 3 Ingredients / Cuisines',
                                          choices=[('Tomato', 'Tomato'),
                                                   ('Egg', 'Egg'),
                                                   ('Mushroom', 'Mushroom'),
                                                   ('Italian', 'Italian'),
                                                   ('Chinese', 'Chinese')],
                                          option_widget=widgets.CheckboxInput())
    dietary_restrictions = SelectField('Dietary Restrictions', choices=[('none', 'None'), ('Halal', 'Halal'), ('vegetarian', 'Vegetarian')])
    submit = SubmitField('Submit')

    def validate_top_preferences(form, field):
        if len(field.data) != 3:
            raise ValidationError('Please select exactly three preferences.')
