from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, HiddenField, validators
from wtforms.fields import DateField, FloatField, IntegerField, PasswordField, BooleanField, FileField
from wtforms.validators import ValidationError, NumberRange


class CreateUser(Form):
    name = StringField([validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    email = StringField([validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Email"})
    phno = StringField([validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Phone Number"})
    register_password = PasswordField([validators.Length(min=8, max=15), validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField([validators.Length(min=8, max=15), validators.DataRequired()], render_kw={"placeholder": "Confirm Password"})

class LoginUser(Form):
    name = StringField([validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    email = StringField([validators.Length(min=1, max=50), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField([validators.Length(min=8, max=15), validators.DataRequired()], render_kw={"placeholder": "Password"})
