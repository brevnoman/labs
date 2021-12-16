from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from mainapp.config import Config
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
# from flask_restful import Api, reqparse
# from mainapp.api_routes import QuestionAPI

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
ma = Marshmallow(app)
# api = Api(app)
# parser = reqparse.RequestParser()
# parser.add_argument('task')
# api.add_resource(QuestionAPI, '/api/questions')


from mainapp import routes, models, schema, api_routes
