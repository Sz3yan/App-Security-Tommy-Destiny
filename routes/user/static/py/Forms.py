from flask_wtf import RecaptchaField
from wtforms import Form, StringField, validators
from wtforms.fields import PasswordField
from wtforms.validators import ValidationError, NumberRange
from flask_wtf.csrf import CSRFProtect


class CreateUser(Form):
    name = StringField([validators.Length(min=1, max=30), validators.Regexp(regex="[a-zA-Z0-9-_]{4, 24}"), validators.DataRequired()], render_kw={"placeholder": "First Name"})
    email = StringField([validators.Length(min=1, max=30), validators.DataRequired()], render_kw={"placeholder": "Email"})
    phno = StringField([validators.Length(min=1, max=20), validators.DataRequired()], render_kw={"placeholder": "Phone Number"})
    register_password = PasswordField([validators.Length(min=8, max=15), validators.Regexp(regex="(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}"), validators.DataRequired()], 
                        render_kw={"placeholder": "Password"})
    confirm_password = PasswordField([validators.Length(min=8, max=15), validators.Regexp(regex="(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}"),validators.EqualTo('register_password', message='Passwords must match'),
                        validators.DataRequired()], render_kw={"placeholder": "Confirm Password"})
    recaptcha = RecaptchaField()

class TwoFactorAuth(Form):
    phno = StringField([validators.Length(min=1, max=20), validators.DataRequired()], render_kw={"placeholder": "Phone Number"})

class EnterOTP(Form):
    otp = PasswordField([validators.Length(min=8, max=15), validators.DataRequired()], render_kw={"placeholder": "OTP"})

class LoginUser(Form):
    email = StringField([validators.Length(min=1, max=30), validators.DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField([validators.Length(min=8, max=15), validators.DataRequired()], render_kw={"placeholder": "Password"})
    recaptcha = RecaptchaField()