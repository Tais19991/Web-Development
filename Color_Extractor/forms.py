from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


class UploadForm(FlaskForm):
    file = FileField('')
    submit = SubmitField("Upload image")