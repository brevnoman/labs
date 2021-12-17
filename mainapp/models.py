from mainapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mainapp import login

interview_question = db.Table('interview_question',
                              db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
                              db.Column('interview_id', db.Integer, db.ForeignKey('interviews.id'), primary_key=True)
                              )

interview_user = db.Table('interview_user',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('interview_id', db.Integer, db.ForeignKey('interviews.id'), primary_key=True)
                          )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(False))

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_selection_list():
        result = []
        for i in User.query.all():
            result.append((f"{i.id}", f"{i.first_name} {i.last_name}"))
        return result


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_description = db.Column(db.Text)
    answer = db.Column(db.String(64))
    max_grade = db.Column(db.Integer)
    short_description = db.Column(db.String(128))

    def __repr__(self):
        return f"{self.short_description}"

    @staticmethod
    def get_selection_list():
        result = []
        for i in Question.query.all():
            result.append((f"{i.id}", f"{i.short_description}"))
        return result


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(64), nullable=False)
    question_list = db.relationship('Question', secondary=interview_question, lazy='subquery',
                                    backref=db.backref('interviews', lazy=True))
    interviewers = db.relationship('User', secondary=interview_user, lazy='subquery',
                                   backref=db.backref('interviews', lazy=True))
    result_grade = db.Column(db.Float(precision=2))

    def __repr__(self):
        return f"{self.candidate_name}"

    @staticmethod
    def get_selection_list():
        result = []
        for i in Interview.query.all():
            result.append((f"{i.id}", f"{i.candidate_name}"))
        return result

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", backref="grades")
    interviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    interviewer = db.relationship("User", backref="grades")
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'))
    interview = db.relationship("Interview", backref="grades")
    grade = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"{self.interviewer} give {self.interview} {self.grade}, for {self.question}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))