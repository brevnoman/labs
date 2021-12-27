from flask import Flask
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_login import LoginManager, current_user
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from mainapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
ma = Marshmallow(app)
api = Api(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='interview', template_mode='bootstrap3')

from mainapp import routes, models, schema, api_routes, api_routes

if not models.User.query.filter_by(is_admin=True).all():
    user = models.User(username="admin", is_admin=True)
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()


class AdminModelView(sqla.ModelView):
    page_size = 50

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        return current_user.is_authenticated


class UserModelView(AdminModelView):

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AdminModelView(models.User, db.session))
admin.add_view(UserModelView(models.Grade, db.session))
admin.add_view(UserModelView(models.Interview, db.session))
admin.add_view(UserModelView(models.Question, db.session))

api.add_resource(api_routes.UserApi, '/api/user')
api.add_resource(api_routes.GradesApi, '/api/grade')
api.add_resource(api_routes.QuestionApi, '/api/question')
api.add_resource(api_routes.InterviewApi, '/api/interview')
api.add_resource(api_routes.LoginApi, '/api/login')
api.add_resource(api_routes.LogoutApi, '/api/logout')
