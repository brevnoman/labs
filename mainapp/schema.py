from mainapp import ma
from mainapp.models import User, Grade, Interview, Question
from marshmallow import fields, post_load, validate
from flask_restful import Resource


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = fields.Str(validate=[validate.Length(64)], required=True)
    email = fields.Str(required=True)
    first_name = fields.Str(validate=[validate.Length(64)], required=True)
    last_name = fields.Str(validate=[validate.Length(64)], required=True)
    password_hash = fields.Str(validate=[validate.Length(255)], required=True)
    is_admin = fields.Boolean(default=False, required=True)

class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade


class InterviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interview


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
