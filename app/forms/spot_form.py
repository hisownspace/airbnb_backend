from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField
from wtforms.validators import InputRequired


class SpotForm(FlaskForm):
    address = StringField("Address", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])
    country = StringField("Country", validators=[InputRequired()])
    lat = FloatField("Latitude", validators=[InputRequired()])
    lng = FloatField("Longitude", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    price = IntegerField("Price", validators=[InputRequired()])
