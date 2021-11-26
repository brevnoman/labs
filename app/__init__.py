from flask import Flask
# from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes