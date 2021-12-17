from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify, request
from mainapp import app, db
from mainapp.models import User, Grade, Interview, Question
from mainapp.schema import UserSchema, GradeSchema, InterviewSchema, QuestionSchema
# from mainapp.models import Question
#
#
# class QuestionAPI(Resource):
#
#     def get(self):
#         result = Question.query.all()
#         return jsonify(result)


@app.route('/api/grades/<int:user_id>')
def grades_api(user_id):
    grades = Grade.query.filter_by(interviewer_id=user_id).all()
    grades_schema = GradeSchema(many=True)
    output = grades_schema.dump(grades)
    return jsonify(output)

@app.route('/api/interview')
def interview_api():
    interviews = Interview.query.all()
    interview_schema = InterviewSchema(many=True)
    output = interview_schema.dump(interviews)
    return jsonify(output)

@app.route('/api/questions')
def question_api():
    questions = Question.query.all()
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify(output)


# user_args = reqparse.RequestParser()
# # user_args.add_argument('id', type=int, required=True)
# user_args.add_argument('username', type=int, required=True)
# user_args.add_argument("email", type=str, required=True)
# user_args.add_argument("first_name", type=str, required=True)
# user_args.add_argument("last_name", type=str, required=True)
# user_args.add_argument("is_admin", type=bool, required=True)
#
# user_fields = {
#     'id': fields.Integer(),
#     'username': fields.String(),
#     'email': fields.String(),
#     'first_name': fields.String(),
#     'last_name': fields.String(),
#     'password': fields.String(),
#     'is_admin': fields.Boolean()
# }

class UserApi(Resource):

    def get(self):
        args = ""
        for key, value in request.args.items():
            print(key, value)
            args += f"{key}={value},"
        users = eval("User.query.filter_by(" + args[:-1] + ").all()")
        users_schema = UserSchema(many=True)
        output = users_schema.dump(users)
        return jsonify(output)

    def put(self):
        args = ""
        for key, value in request.args.items():
            if key == 'password':
                continue
            args += f"{key}={value},"
        user = eval("User(" + args[:-1] + ")")
        user.set_password(request.args.get('password'))
        users_schema = UserSchema()
        output = users_schema.dump(user)
        db.session.add(user)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        user = eval("User.query.filter_by(" + args[:-1] + ").first()")
        db.session.delete(user)
        db.session.commit()
        return {'user': 'deleted successful'}

    def patch(self):
        args = ""

        for key, value in request.args.items():
            args += f"{key}={value},"
        user = eval("User.query.filter_by(" + args[:-1] + ").first()")
        print(request.form.to_dict())
        for key, value in request.form.items():
            if key == "password":
                exec(f"user.set_password({value})")
                continue
            exec(f"user.{key} = {value}")
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

    def get(self):
        args = ""
        for key, value in request.args.items():
            print(key, value)
            args += f"{key}={value},"
        grades = eval("Grade.query.filter_by(" + args[:-1] + ").all()")
        grades_schema = GradeSchema(many=True)
        output = grades_schema.dump(grades)
        return jsonify(output)

    def put(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        grade = eval("Grade(" + args[:-1] + ")")
        db.session.add(grade)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        grade = eval("Grade.query.filter_by(" + args[:-1] + ").first()")
        db.session.delete(grade)
        db.session.commit()
        return {'grade': 'deleted successful'}

    def patch(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        grade = eval("Grade.query.filter_by(" + args[:-1] + ").first()")
        for key, value in request.form.items():
            exec(f"grade.{key} = {value}")
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

    def get(self):
        args = ""
        for key, value in request.args.items():
            print(key, value)
            args += f"{key}={value},"
        print(args)
        interviews = eval("Interview.query.filter_by(" + args[:-1] + ").all()")
        grades_schema = InterviewSchema(many=True)
        output = grades_schema.dump(interviews)
        return jsonify(output)

    def put(self):
        args = ""
        interviewers = []
        questions = []
        for key, value in request.args.items():
            if key == "interviewers":
                for user in eval(value):
                    print("tut user sidit >", type(value))
                    interviewer = User.query.filter_by(id=int(user["id"])).first()
                    interviewers.append(interviewer)
                # args += f"interviewers={interviewers},"
                continue
            if key == "question_list":
                for question_object in eval(value):
                    question = Question.query.filter_by(id=int(question_object['id'])).first()
                    questions.append(question)
                # args += f"question_list={questions},"
                continue
            args += f"{key}={value},"
        print(args)
        interview = eval("Interview(" + args[:-1] + ")")
        if interviewers:
            interview.interviewers = interviewers
        if questions:
            interview.question_list = questions
        db.session.add(interview)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        interview = eval("Interview.query.filter_by(" + args[:-1] + ").first()")
        db.session.delete(interview)
        db.session.commit()
        return {'grade': 'deleted successful'}

    def patch(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        interview = eval("Interview.query.filter_by(" + args[:-1] + ").first()")
        for key, value in request.form.items():
            exec(f"interview.{key} = {value}")
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

    def get(self):
        args = ""
        for key, value in request.args.items():
            print(key, value)
            args += f"{key}={value},"
        questions = eval("Question.query.filter_by(" + args[:-1] + ").all()")
        questions_schema = QuestionSchema(many=True)
        output = questions_schema.dump(questions)
        return jsonify(output)

    def put(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        question = eval("Question(" + args[:-1] + ")")
        db.session.add(question)
        db.session.commit()
        return {'result': 'done'}

    def delete(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        question = eval("Question.query.filter_by(" + args[:-1] + ").first()")
        db.session.delete(question)
        db.session.commit()
        return {'question': 'deleted successful'}

    def patch(self):
        args = ""
        for key, value in request.args.items():
            args += f"{key}={value},"
        question = eval("Question.query.filter_by(" + args[:-1] + ").first()")
        for key, value in request.form.items():
            exec(f"question.{key} = {value}")
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