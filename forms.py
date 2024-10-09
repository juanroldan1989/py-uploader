from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

# Form for uploading files
class UploadForm(FlaskForm):
  file = FileField("File", validators=[DataRequired()])
  submit = SubmitField("Upload")
