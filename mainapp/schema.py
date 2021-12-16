from mainapp import ma
from mainapp.models import User, Grade, Interview, Question


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade


class InterviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Interview


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
