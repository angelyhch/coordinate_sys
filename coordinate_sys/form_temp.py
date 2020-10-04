from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField



class CheckBox(FlaskForm):

    ls = ['aaaa', 'bbbb', 'cccc', 'dddde']

    aaaa = BooleanField(ls[0], render_kw={'value': ls[0]})
    bbbb = BooleanField(ls[1], render_kw={'value': ls[1]})
    cccc = BooleanField(ls[2], render_kw={'value': ls[2]})
    dddd = BooleanField(ls[3], render_kw={'value': ls[3]})
    submit = SubmitField('submit')