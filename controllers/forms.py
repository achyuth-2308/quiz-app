from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    submit = SubmitField('Create Subject')

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    submit = SubmitField('Create Chapter')