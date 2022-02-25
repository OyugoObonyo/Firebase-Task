from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class UploadForm(FlaskForm):
    """
    Form that handles the upload file route
    """
    file = FileField('File', validators=[DataRequired(), FileAllowed(['pdf'])])
    submit = SubmitField('Upload file')
