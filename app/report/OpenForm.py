from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class OpenForm(Form):
    path = StringField('The report to open:', validators=[DataRequired(message='The report path can not be empty.')])