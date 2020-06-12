from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError

from application.models import User


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    first_name = StringField("First name",validators=[DataRequired()])
    last_name = StringField("last name",validators=[DataRequired()])
    role_id  =  StringField("Role Id",validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self,email):
        user=User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use.Pick another one")