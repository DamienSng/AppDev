from wtforms import Form, StringField, TextAreaField, validators, FileField, RadioField

class CreateRecipeForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=150), validators.DataRequired()])
    skill = RadioField('Skill', choices=[('Easy', 'Easy'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')], validators=[validators.DataRequired()])
    time = StringField('Time', [validators.Length(min=1, max=150), validators.DataRequired()])
    cuisine = StringField('Cuisine', [validators.Length(min=1, max=150), validators.DataRequired()])
    instruction = TextAreaField('Instructions', [validators.DataRequired()])
    ingredient = TextAreaField('Ingredients', [validators.DataRequired()])
    alt = TextAreaField('Alternative Ingredients', [validators.Optional()])
    optional = TextAreaField('Optional Ingredients', [validators.Optional()])
    image = FileField('Image', [validators.DataRequired()])
