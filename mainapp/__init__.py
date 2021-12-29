from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
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


@login.unauthorized_handler
def unauthorized_callback():
    return {"error": "you need to login first"}


from mainapp import utils, routes, models, schema, api_routes, api_routes, admin

if not models.User.query.filter_by(is_admin=True).all():
    user = models.User(username="admin", is_admin=True)
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
