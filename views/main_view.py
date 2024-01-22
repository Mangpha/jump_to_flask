from flask import Blueprint

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/hello")
def Hello():
    return "Hello"


@bp.route("/")
def index():
    return "Index"
