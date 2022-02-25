# library -> secure session form with csrf protection
from flask_wtf import FlaskForm

# library -> validation and rendering forms in app
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)

# script -> database model of users database(sqlite)
from .models import User

# Form class:
#   input: FlaskForm
#   return: none
# Note: Structure of registraion form sqlite -> admin level
class RegistrationForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    username = StringField("username", validators=[DataRequired()])
    surname = StringField("surname", validators=[DataRequired()])
    title = StringField("title")
    department = StringField("department")
    role = StringField("role", validators=[DataRequired()])
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=4, max=40)]
    )
    password2 = PasswordField(
        "repeat password",
        validators=[DataRequired(), Length(min=4, max=40), EqualTo("password")],
    )

    register = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


# Form class:
#   input: FlaskForm
#   return: none
# Note: Structure of login form sqlite -> non-user level
class LoginForm(FlaskForm):
    # for brute_force testing
    # class Meta:
    #    csrf = False

    email = StringField("email", validators=[InputRequired(), Length(min=4, max=40)])
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=4, max=40)]
    )
    submit = SubmitField("Sign in")


# Form class:
#   input: FlaskForm
#   return: none
# Note: Structure of find patient form in db2 -> user level
class SearchForm(FlaskForm):
    email = StringField("email")
    surname = StringField("surname")
    session_token = StringField("session_token")
    search = SubmitField("Search")


# Form class:
#   input: FlaskForm
#   return: none
# Note: Structure of find patient form in db2 -> user level
class SearchPatientForm(FlaskForm):
    search_data = StringField("search_data", validators=[DataRequired()])
    search = SubmitField("Search")
