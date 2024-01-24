from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
from datetime import datetime

from main import db
from models import Board
from utils.Forms import AnswerForm, QuestionForm

bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    question_list = Board.Question.query.order_by(Board.Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template("question/question_list.html", question_list=question_list)


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    question = Board.Question.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/create/", methods=("GET", "POST"))
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Board.Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("question/question_form.html", form=form)
