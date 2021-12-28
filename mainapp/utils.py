from sqlalchemy import event, inspect

from mainapp import db
from mainapp.models import Grade, Interview


def update_grade(target, value, oldvalue, initiator):
    interview = Interview.query.filter_by(id=target.interview_id).first()
    num_of_interviewers = len(interview.interviewers)
    interview.result_grade = ((interview.result_grade * num_of_interviewers) + value - oldvalue) / num_of_interviewers
    db.session.commit()


def remove_grade_question(target, value, initiator):
    for grade in target.grades:
        if grade.question == value:
            db.session.delete(grade)


def remove_grade_user(target, value, initiator):
    for grade in target.grades:
        if grade.interviewer == value:
            db.session.delete(grade)


def create_grades_from_question(target, value, initiator):
    db.session.flush()
    for user in target.interviewers:
        if not Grade.query.filter_by(
                question=value,
                interviewer=user,
                interview=target
        ).first():
            grade = Grade(
                question=value,
                interviewer=user,
                interview_id=target.id
            )
            db.session.add(grade)


def create_grades_from_user(target, value, initiator):
    db.session.flush()
    if Interview.query.filter_by(id=target.id).first():
        for question in target.question_list:
            if not Grade.query.filter_by(
                    question=question,
                    interviewer=value,
                    interview=target
            ).first():
                grade = Grade(
                    question=question,
                    interviewer=value,
                    interview_id=target.id
                )
                db.session.add(grade)


def create_grades_when_create(mapper, connection, target):
    for interviewer in target.interviewers:
        for question in target.question_list:
            if not Grade.query.filter_by(
                    question=question,
                    interviewer=interviewer,
                    interview_id=target.id
            ).first():
                grade = Grade(
                    question=question,
                    interviewer=interviewer,
                    interview_id=target.id
                )
                db.session.add(grade)


event.listen(inspect(Grade).column_attrs['grade'], "set", update_grade)
with db.session.no_autoflush:
    event.listen(inspect(Interview).relationships["interviewers"], 'append', create_grades_from_user)
    event.listen(inspect(Interview).relationships["question_list"], "append", create_grades_from_question)
event.listen(Interview, "after_insert", create_grades_when_create)
event.listen(inspect(Interview).relationships["interviewers"], 'remove', remove_grade_user)
event.listen(inspect(Interview).relationships["question_list"], "remove", remove_grade_question)

"""
some problems with events, if i check for append it cause error in object creation
"""
