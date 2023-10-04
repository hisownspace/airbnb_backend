from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError

from app.models.users import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    def validate_password(form, field):
        user = User.query.filter(User.username == form.username.data).first()
        print(user.to_dict())
        if not user.check_password(field.data):
            raise ValidationError("Username and password do not match")
