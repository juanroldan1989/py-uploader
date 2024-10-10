# This file contains the form class for uploading files.
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
  file = FileField("File", validators=[
    DataRequired(),
    FileAllowed(["jpg", "png"], "JPG and PNG files only!"),
    FileSize(max_size=2 * 1024 * 1024, message="File size must be less than 2MB")
  ])
  submit = SubmitField("Upload")
