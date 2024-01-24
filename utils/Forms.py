from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


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
