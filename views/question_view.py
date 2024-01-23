from flask import Blueprint, render_template
from models import Board

bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")
def _list():
    question_list = Board.Question.query.order_by(Board.Question.create_date.desc())
    return render_template("question/question_list.html", question_list=question_list)


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    question = Board.Question.query.get_or_404(question_id)
    return render_template("question/question_detail.html", question=question)
