from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class RunForm(Form):
    app = StringField('The test group to run:', validators=[DataRequired()])