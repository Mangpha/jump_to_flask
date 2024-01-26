from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from datetime import datetime

from main import db
from models.Board import Question, Answer
from utils.Forms import AnswerForm
from views.auth_view import login_required

bp = Blueprint("answer", __name__, url_prefix="/answer")


@bp.route("/create/<int:question_id>", methods=("POST",))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form["content"]
        answer = Answer(
            question=question, content=content, create_date=datetime.now(), user=g.user
        )
        db.session.add(answer)
        db.session.commit()
        return redirect(
            "{}#answer_{}".format(
                url_for("question.detail", question_id=question_id), answer.id
            )
        )
    return render_template(
        "question/question_detail.html", question=question, form=form
    )


@bp.route("/modify/<int:answer_id>", methods=("GET", "POST"))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash("Permission Denied")
        return redirect(url_for("question.detail", question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.update_date = datetime.now()
            db.session.commit()
            return redirect(
                "{}#answer_{}".format(
                    url_for("question.detail", question_id=answer.question.id),
                    answer.id,
                )
            )
    else:
        form = AnswerForm(obj=answer)
    return render_template("answer/answer_form.html", form=form)


@bp.route("/delete/<int:answer_id>")
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash("Permission Denied")
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for("question.detail", question_id=answer.question.id))


@bp.route("/vote/<int:answer_id>")
@login_required
def vote(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user == answer.user:
        flash("Cannot vote your comment")
    else:
        answer.voter.append(g.user)
        db.session.commit()

    return redirect(
        "{}#answer_{}".format(
            url_for("question.detail", question_id=answer.question.id), answer.id
        )
    )
