from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, validators, BooleanField
from wtforms.validators import input_required, ValidationError


class ScheduleForm(Form):

    name = StringField(label="Name", validators=[validators.input_required()])
    url = StringField(label="Url", validators=[validators.input_required()])
    check_interval = IntegerField(label="Check interval", validators=[validators.input_required()])
    active = BooleanField(label="Active", default=False)
