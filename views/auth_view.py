from flask import Blueprint, render_template, url_for, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from main import db
from models.User import User
from utils.Forms import UserCreateForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("Exist User")
    return render_template("auth/signup.html", form=form)
