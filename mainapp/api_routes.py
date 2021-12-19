from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify, request
from mainapp import app, db
from mainapp.models import User, Grade, Interview, Question
from mainapp.schema import UserSchema, GradeSchema, InterviewSchema, QuestionSchema


class UserApi(Resource):

    def get_user_query(self, args):
        print(args.to_dict())
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

    def edit_user(self, user, form):
        print(form.to_dict())
        if form.get("username"):
            user.username = form.get('username')
        if form.get('email'):
            user.email = form.get('email')
        if form.get("first_name"):
            user.first_name = form.get('first_name')
        if form.get("last_name"):
            user.last_name = form.get('last_name')
        return user

    def get(self):
        args = request.args
        users = self.get_user_query(args=args).all()
        users_schema = UserSchema(many=True)
        output = users_schema.dump(users)
        return jsonify(output)

    def put(self):
        form = request.args
        user = User()
        user = self.edit_user(user=user, form=form)
        user.set_password(request.args.get('password'))
        db.session.add(user)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = request.args
        user = self.get_user_query(args).first()
        db.session.delete(user)
        db.session.commit()
        return {'user': 'deleted successful'}

    def patch(self):
        args = request.args
        user = self.get_user_query(args)
        form = request.form
        user = self.edit_user(user, form)
        users_schema = UserSchema()
        output = users_schema.dump(user)
        db.session.commit()
        return jsonify(output)

    def post(self):  # what should we do by POST method?
        changes = request.form
        print(changes)
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        user = eval("User.query.filter_by(" + args[:-1] + ").all()")

        users_schema = UserSchema(many=True)
        output = users_schema.dump(user)
        return jsonify(output)


class GradesApi(Resource):

    def get_grades_query(self, args):
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

    def edit_grade(self, grade, form):
        if form.get("question_id"):
            grade.question_id = form.get('question_id')
        if form.get('interviewer_id'):
            grade.interviewer_id = form.get('interviewer_id')
        if form.get("interview_id"):
            grade.interview_id = form.get('interview_id')
        if form.get("grade"):
            grade.grade = form.get('grade')
        return grade

    def get(self):
        args = request.args
        grades = self.get_grades_query(args=args).all()
        grades_schema = GradeSchema(many=True)
        output = grades_schema.dump(grades)
        return jsonify(output)

    def put(self):
        form = request.args
        grade = Grade()
        grade = self.edit_grade(grade=grade, form=form)
        db.session.add(grade)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = request.args
        grade = self.get_grades_query(args=args).first()
        db.session.delete(grade)
        db.session.commit()
        return {'grade': 'deleted successful'}

    def patch(self):
        args = request.args
        grade = self.get_grades_query(args).first()
        form = request.form
        grade = self.edit_grade(grade=grade, form=form)
        grade_shema = GradeSchema()
        output = grade_shema.dump(grade)
        db.session.commit()
        return jsonify(output)

    def post(self):  # what should we do by POST method?
        changes = request.form
        print(changes)
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        grade = eval("Grade.query.filter_by(" + args[:-1] + ").all()")

        grades_schema = GradeSchema(many=True)
        output = grades_schema.dump(grade)
        return jsonify(output)


class InterviewApi(Resource):

    def get_interviews_query(self, args):
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

    def edit_interview(self, interview, form):
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
                interview.question_list.append(Question.query.filter_by(id=int(form.get('add_question_id'))).first())
        if form.get('exclude_question_id'):
            if Question.query.filter_by(id=int(form.get('exclude_question_id'))).first() in interview.question_list:
                interview.question_list.remove(Question.query.filter_by(id=int(form.get('exclude_question_id'))).first())
        if form.get('add_interviewer_id'):
           if User.query.filter_by(id=int(form.get('add_interviewer_id'))).first() not in interview.interviewers:
                interview.interviewers.append(User.query.filter_by(id=int(form.get('add_interviewer_id'))).first())
        if form.get('exclude_interviewer_id'):
            if User.query.filter_by(id=int(form.get('exclude_interviewer_id'))).first() in interview.interviewers:
                interview.interviewers.remove(User.query.filter_by(id=int(form.get('exclude_interviewer_id'))).first())
        return interview

    def get(self):
        args = request.args
        interviews = self.get_interviews_query(args)
        interviews_schema = InterviewSchema(many=True)
        output = interviews_schema.dump(interviews)
        return jsonify(output)

    def put(self):
        form = request.args
        interview = Interview()
        interview = self.edit_interview(form=form, interview=interview)
        db.session.add(interview)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = request.args
        interview = self.get_interviews_query(args).first()
        db.session.delete(interview)
        db.session.commit()
        return {'grade': 'deleted successful'}

    def patch(self):
        args = request.args
        interview = self.get_interviews_query(args=args).first()
        form = request.form
        interview = self.edit_interview(interview=interview, form=form)
        interview_schema = InterviewSchema()
        output = interview_schema.dump(interview)
        db.session.commit()
        return jsonify(output)

    def post(self):  # what should we do by POST method?
        changes = request.form
        print(changes)
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        interview = eval("Interview.query.filter_by(" + args[:-1] + ").all()")

        interviews_schema = InterviewSchema(many=True)
        output = interviews_schema.dump(interview)
        return jsonify(output)


class QuestionApi(Resource):

    def get_question_query(self, args):
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

    def edit_question(self, question, form):
        if form.get("question_description"):
            question.question_description = form.get('question_description')
        if form.get('answer'):
            question.answer = form.get('answer')
        if form.get("max_grade"):
            question.max_grade = form.get('max_grade')
        if form.get("short_description"):
            question.short_description = form.get('short_description')
        return question

    def get(self):
        args = request.args
        questions = self.get_question_query(args=args).all()
        questions_schema = QuestionSchema(many=True)
        output = questions_schema.dump(questions)
        return jsonify(output)

    def put(self):
        form = request.args
        question = Question()
        question = self.edit_question(question=question, form=form)
        db.session.add(question)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = request.args
        question = self.get_question_query(args=args).first()
        db.session.delete(question)
        db.session.commit()
        return {'question': 'deleted successful'}

    def patch(self):
        args = request.args
        question = self.get_question_query(args=args).first()
        form = request.form
        question = self.edit_question(question=question, form=form)
        question_shema = QuestionSchema()
        output = question_shema.dump(question)
        db.session.commit()
        return jsonify(output)

    def post(self):  # what should we do by POST method?
        changes = request.form
        print(changes)
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        questions = eval("Question.query.filter_by(" + args[:-1] + ").all()")

        questions_schema = QuestionSchema(many=True)
        output = questions_schema.dump(questions)
        return jsonify(output)