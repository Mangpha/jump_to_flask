from flask import Blueprint, render_template, url_for, request, g, flash
from werkzeug.utils import redirect
from datetime import datetime

from main import db
from models import Board, User
from utils.Forms import AnswerForm, QuestionForm
from views.auth_view import login_required

bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")
    question_list = Board.Question.query.order_by(Board.Question.create_date.desc())
    if kw:
        search = "%%{}%%".format(kw)
        sub_query = (
            db.session.query(
                Board.Answer.question_id, Board.Answer.content, User.User.username
            )
            .join(User.User, Board.Answer.user_id == User.User.id)
            .subquery()
        )
        question_list = (
            question_list.join(User.User)
            .outerjoin(sub_query, sub_query.c.question_id == Board.Question.id)
            .filter(
                Board.Question.subject.ilike(search)
                | Board.Question.content.ilike(search)
                | User.User.username.ilike(search)
                | sub_query.c.content.ilike(search)
                | sub_query.c.username.ilike(search)
            )
            .distinct()
        )

    question_list = question_list.paginate(page=page, per_page=10)
    return render_template(
        "question/question_list.html", question_list=question_list, page=page, kw=kw
    )


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    question = Board.Question.query.get_or_404(question_id)
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/create/", methods=("GET", "POST"))
@login_required
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Board.Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user=g.user,
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("question/question_form.html", form=form)


@bp.route("/modify/<int:question_id>", methods=("GET", "POST"))
@login_required
def modify(question_id):
    question = Board.Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("Permission Denied")
        return redirect(url_for("question.detail", question_id=question_id))
    if request.method == "POST":
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.update_date = datetime.now()
            db.session.commit()
            return redirect(url_for("question.detail", question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template("question/question_form.html", form=form)


@bp.route("/delete/<int:question_id>")
@login_required
def delete(question_id):
    question = Board.Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("Permission Denied")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("question._list"))


@bp.route("/vote/<int:question_id>/")
@login_required
def vote(question_id):
    _question = Board.Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash("Cannot vote your article")
    else:
        _question.voter.append(g.user)
        db.session.commit()

    return redirect(url_for("question.detail", question_id=question_id))
