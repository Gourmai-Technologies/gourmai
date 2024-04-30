# WTForms #
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError, InputRequired, Optional

# Contact Us form Class #
class ContactUsForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

# Contact Us form Class #
class messageeForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
