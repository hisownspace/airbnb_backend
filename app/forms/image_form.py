from urllib.request import urlopen
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired, ValidationError


class ImageForm(FlaskForm):
    url = StringField("URL", validators=[InputRequired()])
    preview = BooleanField("Preview?")

    def validate_url(form, field):
        resource = urlopen(field.data)
        if "image" not in resource.headers.get_content_type():
            raise ValidationError("Please provide a valid image url!")
