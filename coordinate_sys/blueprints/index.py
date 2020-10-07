from flask import redirect, Blueprint, url_for, render_template, request, flash
from coordinate_sys.form_temp import UpLoadFile
import coordinate_sys.models as md
import re
import os
from datetime import datetime

hello_bp = Blueprint('hello', __name__)


@hello_bp.route('/')
def hello():
    vin_list_all = md.read_database().columns.to_list()[3:]
    return render_template('hello.html', vin_list_all=vin_list_all)


@hello_bp.route('/upload_data', methods=['get', 'post'])
def upload_data():
    from coordinate_sys import app
    from coordinate_sys.models import read_excel_data, refresh_database
    upload_form = UpLoadFile()

    if upload_form.validate_on_submit():
        if upload_form.upload_password.data == 'gyz':
            file_req = request.files.get("upload_file")
            file_ext = os.path.splitext(file_req.filename)[1]
            file_save_name = 'data'+file_ext
            full_file_path_name = os.path.join(app.config['UPLOAD_PATH'], file_save_name)
            file_req.save(full_file_path_name)
            last_modify_time1 = os.path.getmtime(full_file_path_name)
            last_modify_time = datetime.fromtimestamp(last_modify_time1)
            flash(f'upload success at {last_modify_time}')
            df = read_excel_data(file_path=full_file_path_name)
            refresh_database(df)
            return render_template('upload_data.html', form=upload_form, file_req=file_req)
        else:
            flash('密码错误！请输入正确口令！')
            return redirect(url_for('hello.upload_data'))
    return render_template('upload_data.html', form=upload_form)


@hello_bp.route('/chart_fig', methods=['get', 'post'])
def chart_fig():
    vin_list1 = request.values.getlist('vin_list')

    point_input = request.values.get("point_select")
    point_input_upper = point_input.upper()
    pattern = '[A-Z]{2}\d{4}[A-Z]'
    point_select = re.findall(pattern, point_input_upper)

    direction = request.values.get('direction')

    df = md.read_database()
    column_head3 = ['特征点号', '方向', '名义值']
    vin_list = column_head3 + vin_list1
    chart_points = md.point_select(df, point_list=point_select, direction=direction, vin_list=vin_list)
    chart_response = md.chart_select_point(select_points_df=chart_points)
    return chart_response


@hello_bp.route('/show_data')
def show_data():
    df = md.read_database()
    cols = df.columns
    # 改列名为6位数字
    newcols = list(cols[:3]) + [x[:17][-6:] for x in cols[3:]]
    df.columns = newcols
    data_html = df.to_html()
    return render_template('show_data.html', data_html=data_html)