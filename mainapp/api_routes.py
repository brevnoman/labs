# from flask_restful import Resource
from flask import jsonify
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

@app.route('/api/grades/<user_id>')
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