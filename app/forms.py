from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField, DateTimeField
from wtforms import BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

class TodolistForm(FlaskForm):
    title = TextField('Title', [Length(max=255)])
    start = DateTimeField('Start', [DataRequired()])
    end = DateTimeField('End')
    location = TextAreaField('Description')
    submit = SubmitField("Save")


class RegistrationForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ContactForm(FlaskForm):
    name = TextField("name", [Length(max=255)])
    email = TextField("email", [Length(max=255)])
    phone = TextField("phone", [Length(max=255)])
    subject = TextField("subject", [Length(max=255)])
    message = TextAreaField('message')
    submit = SubmitField("Save")