from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


class UpLoadFileForm(FlaskForm):
    upload_file = FileField('上传最新三坐标data', validators=[FileRequired(), FileAllowed(['xlsx', 'xlsm'])],
                            render_kw={"accept": ".xlsx, .xlsm"})
    upload_password = PasswordField('上传验证口令')
    submit = SubmitField('确认上传')


class InputPartForm(FlaskForm):
    lingjianhao = StringField('查询零件详细信息，请输入零件号（lingjinahao）：', validators=[DataRequired(), Length(8,12)])
    submit = SubmitField('确认查询')


class UploadTableForm(FlaskForm):
    upload_table = FileField('上传更新数据', validators=[FileRequired(), FileAllowed(['xlsx', 'xlsm'])],
                            render_kw={"accept": ".xlsx, .xlsm"})
    upload_password = PasswordField('上传验证口令')
    submit = SubmitField('确认上传')
