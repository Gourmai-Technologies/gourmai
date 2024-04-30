# WTForms #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError

# Gourmai #
from gourmai.auth.models import Users

# Login Form Class #
class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Registration Form Class #
class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired()])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        check_user = Users.query.filter_by(username=username.data).first()
        if check_user is not None:
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        check_email = Users.query.filter_by(email=email.data).first()
        if check_email is not None:
            raise ValidationError('Email already registered.')