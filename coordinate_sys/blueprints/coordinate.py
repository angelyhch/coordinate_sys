from flask import redirect, Blueprint, url_for, render_template, request, flash, current_app
from coordinate_sys.forms import UpLoadFileForm
from coordinate_sys.extensions import cache
import base64
import qrcode
from io import BytesIO
import coordinate_sys.models as md
import re
import os
from datetime import datetime

coordinate_bp = Blueprint('coordinate', __name__)


@coordinate_bp.route('/')
def index():
    url = request.url
    qr_url = qrcode.make(url)
    qr_buffer = BytesIO()
    qr_url.save(qr_buffer)

    # 最后要用decode转出字符串,因为img标签里存放的是字符串。
    qr_img_data = base64.b64encode(qr_buffer.getvalue()).decode()
    pass
    return render_template('index.html', qr_img_data=qr_img_data)


@coordinate_bp.route('/point_select')
# @cache.cached(timeout=60*30)
def point_select(header_cols=4):
    vin_list_all = md.read_database().columns.to_list()[header_cols:]
    df_warn = md.warning_point()
    data_html = df_warn.to_html()
    return render_template('coordinate/point_select.html', vin_list_all=vin_list_all, data_html=data_html)


@coordinate_bp.route('/upload_data', methods=['get', 'post'])
def upload_data():
    from coordinate_sys.models import read_excel_data, refresh_database
    upload_form = UpLoadFileForm()

    if upload_form.validate_on_submit():
        if upload_form.upload_password.data == 'gyz':
            file_req = request.files.get("upload_file")
            file_ext = os.path.splitext(file_req.filename)[1]
            file_save_name = 'data'+file_ext
            full_file_path_name = os.path.join(current_app.config.get('UPLOAD_PATH'), file_save_name)
            file_req.save(full_file_path_name)
            last_modify_time1 = os.path.getmtime(full_file_path_name)
            last_modify_time = datetime.fromtimestamp(last_modify_time1)
            flash(f'upload success at {last_modify_time}')
            df = read_excel_data(file_path=full_file_path_name)
            refresh_database(df)
            return redirect('coordinate/upload_data.html', form=upload_form)
        else:
            flash('上传不成功，密码错误了！请输入正确口令！')
            return redirect(url_for('coordinate.upload_data'))
    return render_template('coordinate/upload_data.html', form=upload_form)


@coordinate_bp.route('/chart_fig', methods=['get', 'post'])
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


@coordinate_bp.route('/show_data')
def show_data(header_cols=4):
    df = md.read_database()
    # point_name_dict = md.read_point_name()
    cols = df.columns
    # 改列名为6位数字
    newcols = list(cols[:header_cols]) + [x[:17][-6:] for x in cols[header_cols:]]
    df.columns = newcols
    data_html = df.to_html()
    return render_template('coordinate/show_data.html', data_html=data_html)


@coordinate_bp.route('/warning_point')
def warning_point():
    df_warn = md.warning_point()
    data_html = df_warn.to_html()
    return render_template('coordinate/warning_point.html', data_html=data_html)


# 试试coordinate git
