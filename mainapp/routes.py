from flask import render_template, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user

from mainapp import app, db, login
from mainapp.forms import UserForm, QuestionForm, InterviewForm, GradeForm, LoginForm
from mainapp.models import User, Question, Interview, Grade


@app.route('/')
@app.route('/users')
@login_required
def a():
    query = User.query.all()
    return render_template('index.html', query=query)


@app.route('/add-user', methods=["GET", "POST"])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    is_admin=form.is_admin.data
                    )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("user added")
        return redirect('/add-user')
    return render_template('form.html', form=form)


@app.route('/questions')
@login_required
def questions():
    query = Question.query.all()
    return render_template('index.html', query=query)


@app.route('/add-question', methods=["GET", "POST"])
@login_required
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
@login_required
def interviews():
    query = Interview.query.all()
    return render_template('index.html', query=query)


@app.route('/add-interview', methods=["GET", "POST"])
@login_required
def add_interview():
    form = InterviewForm().new()
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
        db.session.add(interview)
        db.session.commit()
        return redirect('/add-interview')
    return render_template('form.html', form=form)


@app.route('/grades')
@login_required
def grades():
    query = Grade.query.all()
    return render_template('index.html', query=query)


@app.route('/add-grade', methods=["POST", "GET"])
@login_required
def add_grade():
    form = GradeForm().new()
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


@app.route("/login", methods=["GET", "POST"])
def login_route():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.get_password(form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect("/")
            flash("Invalid password")
            return render_template("form.html", form=form)
        flash("Invalid username")
    return render_template("form.html", form=form)


@login_required
@app.route("/logout")
def logout_route():
    logout_user()
    return redirect('/login')


@login.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')
