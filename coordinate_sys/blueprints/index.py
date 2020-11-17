from flask import redirect, Blueprint, url_for, render_template, request, flash
from coordinate_sys.form_temp import UpLoadFile
from coordinate_sys.extensions import cache
import coordinate_sys.models as md
import re
import os
from datetime import datetime

hello_bp = Blueprint('hello', __name__)


@hello_bp.route('/')
@cache.cached(timeout=60*30)
def point_select(header_cols=4):
    point_name_dict = md.read_point_name()
    vin_list_all = md.read_database().columns.to_list()[header_cols:]
    df_warn = md.warning_point()
    data_html = df_warn.to_html()
    return render_template('hello/point_select.html', vin_list_all=vin_list_all, data_html=data_html)


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
            return render_template('hello/upload_data.html', form=upload_form, file_req=file_req)
        else:
            flash('密码错误！请输入正确口令！')
            return redirect(url_for('hello.upload_data'))
    return render_template('hello/upload_data.html', form=upload_form)


@hello_bp.route('/chart_fig', methods=['get', 'post'])
def chart_fig():
    vin_list1 = request.values.getlist('vin_list')

    point_input = request.values.get("point_select")
    point_input_upper = point_input.upper()
    pattern = '[A-Z]{2}\d{4}[A-Z]'
    point_select = re.findall(pattern, point_input_upper)

    direction = request.values.get('direction')

    df = md.read_database()
    column_head4 = ['特征点号', '方向', '测点功能', '名义值']
    vin_list = column_head4 + vin_list1
    chart_points = md.point_select(df, point_list=point_select, direction=direction, vin_list=vin_list)
    chart_response = md.chart_select_point(select_points_df=chart_points)
    return chart_response


@hello_bp.route('/show_data')
def show_data(header_cols=4):
    df = md.read_database()
    # point_name_dict = md.read_point_name()
    cols = df.columns
    # 改列名为6位数字
    newcols = list(cols[:header_cols]) + [x[:17][-6:] for x in cols[header_cols:]]
    df.columns = newcols
    # df.insert(2, '测点功能', df['特征点号'])
    # df['测点功能'] = [point_name_dict.get(x[:6], '未查到') for x in list(df['特征点号'])]
    data_html = df.to_html()
    return render_template('hello/show_data.html', data_html=data_html)


@hello_bp.route('/warning_point')
def warning_point():
    df_warn = md.warning_point()
    data_html = df_warn.to_html()
    return render_template('hello/warning_point.html', data_html=data_html)

