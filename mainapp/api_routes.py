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




@app.route('/api/users')
def user_api():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    output = users_schema.dump(users)
    return jsonify(output)

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


user_args = reqparse.RequestParser()
# user_args.add_argument('id', type=int, required=True)
user_args.add_argument('username', type=int, required=True)
user_args.add_argument("email", type=str, required=True)
user_args.add_argument("first_name", type=str, required=True)
user_args.add_argument("last_name", type=str, required=True)
user_args.add_argument("is_admin", type=bool, required=True)

user_fields = {
    'id': fields.Integer(),
    'username': fields.String(),
    'email': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'password': fields.String(),
    'is_admin': fields.Boolean()
}

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
