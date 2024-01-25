from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField(
        "Title", validators=[DataRequired("Title field is required.")]
    )
    content = TextAreaField(
        "Content", validators=[DataRequired("Content field is required.")]
    )


class AnswerForm(FlaskForm):
    content = TextAreaField(
        "Answer", validators=[DataRequired("Answer field is required.")]
    )


class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("Username field is required."),
            Length(
                min=5,
                max=20,
                message="Username field must be between 5 and 20 characters long.",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password field is required."),
            Length(
                min=6,
                max=30,
                message="Password field must be between 6 and 30 characters long.",
            ),
            EqualTo("password_check", "Passwords do not match."),
        ],
    )
    password_check = PasswordField(
        "Password Check", validators=[DataRequired("Password Check field is required.")]
    )
    email = EmailField(
        "Email", validators=[DataRequired("Email field is required."), Email()]
    )


class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
