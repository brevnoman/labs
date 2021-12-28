from flask import jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful import Resource

from mainapp import db
from mainapp.forms import LoginForm
from mainapp.models import User, Grade, Interview, Question
from mainapp.schema import UserSchema, GradeSchema, InterviewSchema, QuestionSchema


class MainResource(Resource):

    def get_model_query(self):
        pass

    def edit_object(self):
        pass

    def create_object(self):
        pass

    def get_schema(self):
        pass

    @login_required
    def get(self):
        schema = self.get_schema()
        model_schema = schema(many=True)
        if isinstance(model_schema, UserSchema) and not current_user.is_admin:
            return {"error": "you are not admin"}
        args = request.args
        model_objects = self.get_model_query(args=args).all()
        output = model_schema.dump(model_objects)
        return jsonify(output)

    @login_required
    def delete(self):
        if isinstance(self.get_schema()(), UserSchema) and not current_user.is_admin:
            return {"error": "you are not admin"}
        args = request.args
        model_object = self.get_model_query(args).first()
        db.session.delete(model_object)
        db.session.commit()
        return {'success': 'True'}

    @login_required
    def patch(self):
        object_schema = self.get_schema()()
        if isinstance(object_schema, UserSchema) and not current_user.is_admin:
            return {"error": "you are not admin"}
        args = request.args
        model_object = self.get_model_query(args).first()
        form = request.form
        model_object = self.edit_object(model_object, form)
        output = object_schema.dump(model_object)
        db.session.commit()
        return jsonify(output)

    @login_required
    def post(self):
        if isinstance(self.get_schema()(), UserSchema) and not current_user.is_admin:
            return {"error": "you are not admin"}
        form = request.form
        model_object = self.create_object(form=form)
        db.session.add(model_object)
        db.session.commit()
        return {'result': 'done'}


class UserApi(MainResource):

    def get_model_query(self, args):
        users = User.query
        if args.get("id"):
            users = users.filter_by(id=args.get('id'))
        if args.get("username"):
            users = users.filter_by(username=args.get('username'))
        if args.get('email'):
            users = users.filter_by(email=args.get('email'))
        if args.get("first_name"):
            users = users.filter_by(first_name=args.get('first_name'))
        if args.get("last_name"):
            users = users.filter_by(last_name=args.get("last_name"))
        return users

    def edit_object(self, user, form):
        if form.get("username"):
            user.username = form.get('username')
        if form.get('email'):
            user.email = form.get('email')
        if form.get("first_name"):
            user.first_name = form.get('first_name')
        if form.get("last_name"):
            user.last_name = form.get('last_name')
        if form.get("is_admin"):
            if form.get("is_admin") == "True":
                user.is_admin = True
            elif form.get("is_admin") == "False":
                user.is_admin = False
        return user

    def create_object(self, form):
        user = User()
        if not form.get("username") or not form.get("password"):
            raise Exception("no username or password")
        user = self.edit_object(user, form)
        return user

    def get_schema(self):
        return UserSchema


class GradesApi(MainResource):

    def get_model_query(self, args):
        grades = Grade.query
        if args.get("id"):
            grades = grades.filter_by(id=args.get('id'))
        if args.get("question_id"):
            grades = grades.filter_by(question_id=args.get('question_id'))
        if args.get('interviewer_id'):
            grades = grades.filter_by(interviewer_id=args.get('interviewer_id'))
        if args.get("interview_id"):
            grades = grades.filter_by(interview_id=args.get('interview_id'))
        if args.get("grade"):
            grades = grades.filter_by(grade=args.get("grade"))
        return grades

    def edit_object(self, grade, form):
        grade = grade.first()
        if form.get("question_id"):
            grade.question_id = form.get('question_id')
        if form.get('interviewer_id'):
            grade.interviewer_id = form.get('interviewer_id')
        if form.get("interview_id"):
            grade.interview_id = form.get('interview_id')
        if form.get("grade"):
            grade.grade = form.get('grade')
        return grade

    def get_schema(self):
        return GradeSchema

    def create_object(self, form):
        grade = Grade()
        if not form.get("interview_id") or not form.get("interviewer_id") or not form.get("question_id"):
            raise Exception("no")
        grade = self.edit_object(grade=grade, form=form)
        return grade


class InterviewApi(MainResource):

    def get_model_query(self, args):
        interviews = Interview.query
        if args.get("id"):
            interviews = interviews.filter_by(id=args.get('id'))
        if args.get("candidate_name"):
            interviews = interviews.filter_by(candidate_name=args.get('candidate_name'))
        if args.get('result_grade'):
            interviews = interviews.filter_by(result_grade=args.get('result_grade'))
        if args.get("question_id"):
            interviews = interviews.filter(Interview.question_list.any(id=args.get("question_id")))
        if args.get('interviewer_id'):
            interviews = interviews.filter(Interview.interviewers.any(id=args.get("interviewer_id")))
        return interviews

    def edit_object(self, interview, form):
        if form.get("candidate_name"):
            interview.candidate_name = form.get('candidate_name')
        if form.get('result_grade'):
            interview.result_grade = form.get('result_grade')
        if form.get("interview_id"):
            interview.interview_id = form.get('interview_id')
        if form.get("result_grade"):
            interview.result_grade = form.get('result_grade')
        if form.get('add_question_id'):
            if Question.query.filter_by(id=int(form.get('add_question_id'))).first() not in interview.question_list:
                question = Question.query.filter_by(id=int(form.get('add_question_id'))).first()
                interview.question_list.append(question)
        if form.get('exclude_question_id'):
            if Question.query.filter_by(id=int(form.get('exclude_question_id'))).first() in interview.question_list:
                question = Question.query.filter_by(id=int(form.get('exclude_question_id'))).first()
                interview.question_list.remove(question)
        if form.get('add_interviewer_id'):
            if User.query.filter_by(id=int(form.get('add_interviewer_id'))).first() not in interview.interviewers:
                interviewer = User.query.filter_by(id=int(form.get('add_interviewer_id'))).first()
                interview.interviewers.append(interviewer)
        if form.get('exclude_interviewer_id'):
            if User.query.filter_by(id=int(form.get('exclude_interviewer_id'))).first() in interview.interviewers:
                interviewer = User.query.filter_by(id=int(form.get('exclude_interviewer_id'))).first()
                interview.interviewers.remove(interviewer)
        return interview

    def get_schema(self):
        return InterviewSchema

    def create_object(self, form):
        interview = Interview()
        if not form.get("candidate_name"):
            raise Exception("no")
        interview = self.edit_object(interview, form)
        return interview


class QuestionApi(MainResource):

    def get_model_query(self, args):
        question = Question.query
        if args.get("id"):
            question = question.filter_by(id=args.get('id'))
        if args.get("question_description"):
            question = question.filter_by(question_description=args.get('question_description'))
        if args.get('answer'):
            question = question.filter_by(answer=args.get('answer'))
        if args.get("max_grade"):
            question = question.filter_by(max_grade=args.get('max_grade'))
        if args.get("short_description"):
            question = question.filter_by(short_description=args.get("short_description"))
        return question

    def edit_object(self, question, form):
        if form.get("question_description"):
            question.question_description = form.get('question_description')
        if form.get('answer'):
            question.answer = form.get('answer')
        if form.get("max_grade"):
            question.max_grade = form.get('max_grade')
        if form.get("short_description"):
            question.short_description = form.get('short_description')
        return question

    def get_schema(self):
        return QuestionSchema

    def create_object(self, form):
        question = Question()
        if not form.get('candidate_name'):
            raise Exception("no candidate name")
        question = self.edit_object(question, form)
        return question


class LoginApi(Resource):

    def post(self):
        form = LoginForm(data=request.form)
        user = User.query.filter_by(username=form.username.data).first()
        if User.query.filter_by(username=form.username.data).first():
            if user.get_password(form.password.data):
                login_user(user)
                return {"login": "success"}
            return {"error": "invalid password"}
        return {"error": "invalid username"}


class LogoutApi(Resource):

    @login_required
    def post(self):
        logout_user()
        return {"logout": "success"}
