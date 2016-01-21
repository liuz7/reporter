from flask_wtf import Form
from wtforms import SelectField
from wtforms.validators import DataRequired, AnyOf
from app import app_list

class RunForm(Form):
    app = SelectField('The test group to run:', choices=map(lambda x: (x, x), app_list),
        validators=[DataRequired(message='The test group can not be empty.'),
                    AnyOf(app_list, message="Input value is not in valid app list.")])