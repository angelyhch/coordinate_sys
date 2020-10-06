from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CheckBox(FlaskForm):
    ls = ['aaaa', 'bbbb', 'cccc', 'dddde']

    aaaa = BooleanField(ls[0], render_kw={'value': ls[0]})
    bbbb = BooleanField(ls[1], render_kw={'value': ls[1]})
    cccc = BooleanField(ls[2], render_kw={'value': ls[2]})
    dddd = BooleanField(ls[3], render_kw={'value': ls[3]})
    submit = SubmitField('submit')


class UpLoadFile(FlaskForm):
    upload_file = FileField('上传最新三坐标data', validators=[FileRequired(), FileAllowed(['xlsx', 'xlsm'])],
                            render_kw={"accept": ".xlsx, .xlsm"})
    upload_password = PasswordField('上传验证口令')
    submit = SubmitField('确认上传')