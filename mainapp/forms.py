from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields import SelectMultipleField, SelectField
from mainapp.models import Question, Interview, User


class UserForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    first_name = StringField("First Name")
    last_name = StringField("Lask Name")
    password = PasswordField("Password", validators=[DataRequired()])
    is_admin = BooleanField("Admin status", default=False)
    submit = SubmitField("Add")


class QuestionForm(FlaskForm):

    question_description = TextAreaField("Question description", validators=[DataRequired()])
    answer = StringField("Answer", validators=[DataRequired()])
    max_grade = IntegerField("Maximal Grade", validators=[DataRequired()], default=10)
    short_description = StringField("Short description", validators=[DataRequired()])
    submit = SubmitField("Add")


class InterviewForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    candidate_name = StringField('Candidate Name', validators=[DataRequired()])
    question_list = SelectMultipleField("Choose Questions", choices=Question.get_selection_list())
    interviewers = SelectMultipleField("Choose Interviewers", choices=User.get_selection_list())
    submit = SubmitField("Add")

    @classmethod
    def new(cls):
        form = cls()
        form.interviewers.choices = User.get_selection_list()
        form.question_list.choices = Question.get_selection_list()
        return form


class GradeForm(FlaskForm):
    interviewers = SelectField("Choose Interviewers", choices=User.get_selection_list())
    question_list = SelectField("Choose Questions", choices=Question.get_selection_list())
    interviews = SelectField("Choose Interview", choices=Interview.get_selection_list())
    submit = SubmitField('add')

    @classmethod
    def new(cls):
        form = cls()
        form.interviewers.choices = User.get_selection_list()
        form.question_list.choices = Question.get_selection_list()
        form.interviews.choices = Interview.get_selection_list()
        return form