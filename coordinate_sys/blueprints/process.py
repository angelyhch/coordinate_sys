from flask import url_for, render_template, Blueprint, request, flash, redirect, current_app
import qrcode
import os
from coordinate_sys.logger_class import logger
from datetime import datetime
import base64
from io import BytesIO
import numpy as np
from coordinate_sys.extensions import cache
from coordinate_sys.process_model import dbo
from coordinate_sys.forms import InputPartForm, UploadTableForm


process_bp = Blueprint('process', __name__, url_prefix='/process')

info_table_list_0 = ['jig', 'jig_records', 'part', 'renyuanpeixun', 'weldspot', 'tujiao', 'co2', 'torque', 'shebeilvli', 'daoruyanzhengjilu', 'gongju', 'muju']
info_table_list = [(item+'_view') for item in info_table_list_0]
info_table_name_dict = {
    'jig': '夹具清单表',
    'part': '零部件清单表',
    'weldspot': '焊点清单表',
    'daoruyanzhengjilu': '车型导入验证记录',
    'tujiao': '涂胶明细表',
    'muju': '模具明细表',
    'jig_records': '夹具履历表',
    'co2': 'co2焊明细表',
    'torque': '扭矩明细表',
    'gongju': '工具台账表',
    'shebeilvli': '设备履历表',
    'renyuanpeixun': '人员培训记录'
}
info_tableView_name_dict = dict((item[0] + '_view', item[1]) for item in info_table_name_dict.items())

base_table_list_0 = ['controlplan']
base_table_list = [(item + '_view') for item in base_table_list_0]
base_table_name_dict = {
    "controlplan": "控制计划"
}
base_tableView_name_dict = dict((item[0] + '_view', item[1]) for item in base_table_name_dict.items())

# 合并所有表格字典
all_tableView_dict = {}
all_tableView_dict.update(info_tableView_name_dict)
all_tableView_dict.update(base_tableView_name_dict)


@process_bp.route('/')
def stations():
    url = request.url
    qr_url = qrcode.make(url)
    qr_buffer = BytesIO()
    qr_url.save(qr_buffer)

    # 最后要用decode转出字符串,因为img标签里存放的是字符串。
    qr_img_data = base64.b64encode(qr_buffer.getvalue()).decode()

    station_weight_1 = dbo.read_table('station_weight_view', index_col='station')   # 以station为index，读出单列数据
    station_weight_dict = station_weight_1.to_dict()['weight']  # 转换为字典格式

    station_table = dbo.read_table('station_view')
    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    return render_template('process/stations.html', qr_img_data=qr_img_data,
                           station_header=station_header, station_list=station_list,
                           station_weight_dict=station_weight_dict)


@process_bp.route('/info/<string:url>', methods=['get', 'post'])
def info(url):
    file_req = url
    input_part_form = InputPartForm()
    upload_table_form = UploadTableForm()
    if input_part_form.validate_on_submit() or request.form.get('search_lingjianhao'):
        if input_part_form.validate_on_submit():
            lingjinahao = input_part_form.lingjianhao.data
        else:
            # 从station的零件号直接查询零件信息，JS通过动态FORM实现该功能对接到此处
            lingjianhao = request.form.get('search_lingjianhao')
        df_pbom = dbo.read_table('pbom')
        df_part = df_pbom.loc[df_pbom['lingjianhao'] == lingjianhao, ]
        df_part_html = df_part.to_html()
        return df_part_html
    elif upload_table_form.validate_on_submit():
        if upload_table_form.upload_password.data == 'baozhang':
            file_req = request.files.get("upload_table")
            if file_req.filename.startswith(url):
                file_ext = os.path.splitext(file_req.filename)[1]
                file_save_name = url + file_ext
                full_file_path_name = os.path.join(current_app.config.get('TABLE_UPLOAD_PATH'), file_save_name)
                file_req.save(full_file_path_name)
                last_modify_time1 = os.path.getmtime(full_file_path_name)
                last_modify_time = datetime.fromtimestamp(last_modify_time1)
                flash(f'upload success at {last_modify_time}')

                dbo.excel_to_table(file_save_name, url, temp_folder=r"static\process_table_upload_temp")
                ip = request.remote_addr
                user_url = request.url
                logger.warn(f'【ip】{ip} 【url】{user_url}')

                flash(f'最新数据更新时间：{datetime.now().isoformat()}')
                return redirect(url_for('process.info', url=url))
            else:
                flash(f'更新不成功，上传文件名错误，请上传【{url}】数据文件！')
                return redirect(url_for('process.info', url=url))
        else:
            flash('更新不成功，密码错误！请输入正确口令！')
            return redirect(url_for('process.info', url=url))
    else:
        file_req_view = file_req + '_view'
        if file_req_view in all_tableView_dict:
            df = dbo.read_table(file_req_view)
            table_name = all_tableView_dict[file_req_view]
            df_html = df.to_html()
            return render_template('process/info.html', upload_table_form=upload_table_form, input_part_form=input_part_form, df_html=df_html, table=file_req_view, table_name=table_name)
        else:
            return '<h1> 不是信息表！ </h1>'


@process_bp.route('/stations/<station>')
@cache.cached(query_string=True)
def station(station):
    station_dict = {}
    for table in info_table_list:
        df_tb = dbo.read_table(table)
        df_tb_st = df_tb.loc[df_tb['station'] == station, ]
        station_dict[table] = df_tb_st

    # 对搜索出的来的数据进行排序，最多数据排在最上面。
    station_dict = dict(sorted(station_dict.items(), key=lambda x:(x[1].shape[0]), reverse=True))

    return render_template('process/station.html', tableView_name_dict=info_tableView_name_dict, station=station, station_dict=station_dict)
