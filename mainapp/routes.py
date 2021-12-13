from mainapp import app, db
from flask import jsonify
from mainapp.models import User, UserInfo

@app.route('/')
def main_page():
    u = UserInfo.query.all()
    user = User.query.all()
    return f"{user}, {u}"


@app.route('/a')
def a():
    u = UserInfo.query.first()
    u.admin = False
    db.session.commit()
    return "done"
# @app.route('/add')
# def add():
#