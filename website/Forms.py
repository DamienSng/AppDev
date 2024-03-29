from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField,DateField

class CreateUserForm(Form):
    first_name = StringField("First Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField("Last Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField("Gender", [validators.DataRequired()], choices=[(",","Select"), ("F", "Female"), ("M", "Male")], default="")
    membership = RadioField("Membership", choices=[("F", "Fellow"), ("S", "Senior"),("P", "Professional")], default="F")
    remarks = TextAreaField("Remarks", [validators.Optional()])


class CreateCustomerForm(Form):
    first_name = StringField("First Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField("Last Name", [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField("Gender", [validators.DataRequired()], choices=[(",", "Select"), ("F", "Female"), ("M", "Male")], default="")
    email = EmailField("Email", [validators.Email(), validators.DataRequired()])
    date_joined = DateField("Date Joined", format="%Y-%m-%d")
    address = TextAreaField("Mailing Address", [validators.length(max=200), validators.DataRequired()])
    membership = RadioField("Membership", choices=[("F", "Fellow"), ("S", "Senior"), ("P", "Professional")], default="F")
    remarks = TextAreaField("Remarks", [validators.Optional()])



# Start of project
class CreateFeedbackForm(Form):
    username = StringField("Username", [validators.Length(min=1, max=30), validators.DataRequired()])
    email_address = EmailField("Email Address", [validators.Email(), validators.DataRequired()])
    subject = StringField("Subject", [validators.Length(min=1, max=30), validators.DataRequired()])
    feedback = TextAreaField("Feedback", [validators.Length(min=1, max=150), validators.DataRequired()])

class CreateSurveyForm(Form):
    username = StringField("Username", [validators.Length(min=1, max=30), validators.DataRequired()])
    email_address = EmailField("Email Address", [validators.Email(), validators.DataRequired()])
    cuisine = RadioField("Cuisine", choices=[("Chinese", "Chinese"), ("Korean", "Korean"), ("Japanese", "Japanese"), ("Mexican", "Mexican"), ("Thai", "Thai"), ("Indian", "Indian")],
                            default="Chinese")
    recipe_name = TextAreaField("Recipe Name", [validators.Optional()])