# from werkzeug.wrappers import Request, Response
from flask_sqlalchemy import inspect
from sqlalchemy import event

from mainapp import models, db


def update_grade(target, value, oldvalue, initiator):
    print("chtoto")
    interview = models.Interview.query.filter_by(id=target.interview_id).first()
    interview.result_grade = 0
    for grade in models.Grade.query.filter_by(interview_id=target.interview_id).all():
        interview.result_grade += grade.grade
    db.session.commit()


class Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        print("ya tut bil")
        event.listen(inspect(models.Grade).column_attrs['grade'], "commit", update_grade)
        return self.app(environ, start_response)
