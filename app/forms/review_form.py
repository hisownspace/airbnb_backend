from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange


class ReviewForm(FlaskForm):
    review = StringField("Review", validators=[InputRequired()])
    stars = IntegerField(
        "Stars", validators=[InputRequired(), NumberRange(min=1, max=5)]
    )
