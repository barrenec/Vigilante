from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, validators
from wtforms.validators import input_required, ValidationError


class ScheduleForm(Form):

    name = StringField(label="name", validators=[validators.input_required()])
    url = StringField(label="url", validators=[validators.input_required()])
    check_interval = IntegerField(label="checkinterval", validators=[validators.input_required()])