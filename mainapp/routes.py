from mainapp import app, db
from flask import render_template, flash, redirect
from mainapp.models import User, Question, Interview, Grade
from mainapp.forms import UserForm, QuestionForm, InterviewForm, GradeForm


# from flask_login import current_user, login_user

@app.route('/')
def main_page():
    query = User.query.all()
    return render_template('index.html', query=query)


@app.route('/users')
def a():
    query = User.query.all()
    return render_template('index.html', query=query)

@app.route('/add-user', methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data
                    )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("user added")
        return redirect('/add-user')
    return render_template('form.html', form=form)


@app.route('/questions')
def questions():
    query = Question.query.all()
    return render_template('index.html', query=query)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(question_description=form.question_description.data,
                            answer=form.answer.data,
                            max_grade=form.max_grade.data,
                            short_description=form.short_description.data
                            )
        db.session.add(question)
        db.session.commit()
        return redirect('/add-question')
    return render_template('form.html', form=form)


@app.route('/interviews')
def interviews():
    query = Interview.query.all()
    return render_template('index.html', query=query)


@app.route('/add-interview', methods=["GET", "POST"])
def add_interview():
    form = InterviewForm()
    if form.validate_on_submit():
        question_list = []
        interviewers = []
        for question_id in form.question_list.data:
            question = Question.query.filter_by(id=question_id).first()
            question_list.append(question)
        for interviewer_id in form.interviewers.data:
            user = User.query.filter_by(id=interviewer_id).first()
            interviewers.append(user)
        interview = Interview(candidate_name=form.candidate_name.data,
                            question_list=question_list,
                            interviewers=interviewers,
                            )
        all = [interview]
        for user in interviewers:
            for question in question_list:
                grade = Grade(
                    question=question,
                    interviewer=user,
                    interview=interview
                )
                all.append(grade)
        db.session.add_all(all)
        db.session.commit()
        return redirect('/add-interview')
    return render_template('form.html', form=form)

@app.route('/grades')
def grades():
    query = Grade.query.all()
    return render_template('index.html', query=query)



@app.route('/add-grade', methods=["POST", "GET"])
def add_grade():
    form = GradeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.interviewers.data).first()
        question = Question.query.filter_by(id=form.question_list.data).first()
        interview = Interview.query.filter_by(id=form.interviews.data).first()
        grade = Grade(
            interviewer=user,
            question=question,
            interview=interview,
            grade=1
                            )
        db.session.add(grade)
        db.session.commit()
        return redirect('/add-grade')
    return render_template('form.html', form=form)