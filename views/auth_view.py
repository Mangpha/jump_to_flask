from flask import Blueprint, render_template, url_for, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from main import db
from models.User import User
from utils.Forms import UserCreateForm, UserLoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            flash("Exist User")
    return render_template("auth/signup.html", form=form)


@bp.route("/login/", methods=("GET", "POST"))
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "User does not exist."
        elif not check_password_hash(user.password, form.password.data):
            error = "The Password is not correct"
        if error is None:
            session.clear()
            session["user_id"] = user.id
            _next = request.args.get("next", "")
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for("main.index"))
        flash(error)
    return render_template("auth/login.html", form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == "GET" else ""
            return redirect(url_for("auth.login", next=_next))
        return view(*args, **kwargs)

    return wrapped_view
