from main import db

question_voter = db.Table(
    "question_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "question_id",
        db.Integer,
        db.ForeignKey("question.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    update_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("question_set"))
    voter = db.relationship(
        "User", secondary=question_voter, backref=db.backref("question_voter_set")
    )


answer_voter = db.Table(
    "answer_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "answer_id",
        db.Integer,
        db.ForeignKey("answer.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="CASCADE")
    )
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    update_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("answer_set"))
    voter = db.relationship(
        "User", secondary=answer_voter, backref=db.backref("answer_voter_set")
    )
