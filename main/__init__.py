from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from models import Board, User

    # Blue Print
    from views import main_view, question_view, answer_view, auth_view

    app.register_blueprint(question_view.bp)
    app.register_blueprint(main_view.bp)
    app.register_blueprint(answer_view.bp)
    app.register_blueprint(auth_view.bp)

    # Filter
    from utils.filter import format_datetime

    app.jinja_env.filters["datetime"] = format_datetime

    return app
