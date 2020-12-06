from flask import url_for, render_template, Blueprint, request
import qrcode
from PIL import Image
import base64
from io import StringIO, BytesIO
import numpy as np
from coordinate_sys.extensions import cache
from coordinate_sys.process_model import dbo
from coordinate_sys.forms import InputPartForm


process_bp = Blueprint('process', __name__, url_prefix='/process')

info_table_list = ['jig', 'jig_records', 'part', 'weldspot', 'tujiao', 'daoruyanzhengjilu', 'muju']
table_name_dict = {
    'jig': '夹具清单表',
    'part': '零部件清单表',
    'weldspot': '焊点清单表',
    'daoruyanzhengjilu': '车型导入验证记录',
    'tujiao': '涂胶明细表',
    'muju': '模具明细表',
    'jig_records': '夹具履历表'
}


@process_bp.route('/')
def stations():

    url = request.url
    qr_url = qrcode.make(url)
    qr_buffer = BytesIO()
    qr_url.save(qr_buffer)

    # 最后要用decode转出字符串,因为img标签里存放的是字符串。
    qr_img_data = base64.b64encode(qr_buffer.getvalue()).decode()

    station_table = dbo.read_table('station')
    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    return render_template('process/stations.html', qr_img_data=qr_img_data, station_header=station_header, station_list=station_list)


@process_bp.route('/info/<string:url>', methods=['get', 'post'])
def info(url):
    table = url
    input_part_form = InputPartForm()

    if input_part_form.validate_on_submit() or request.form.get('search_lingjianhao'):
        if input_part_form.validate_on_submit():
            lingjinahao = input_part_form.lingjianhao.data
        else:
            lingjianhao = request.form.get('search_lingjianhao')
        df_pbom = dbo.read_table('pbom')
        df_part = df_pbom.loc[df_pbom['lingjianhao'] == lingjianhao, ]
        df_part_html = df_part.to_html()
        return df_part_html
    else:
        if table in info_table_list:
            df = dbo.read_table(table)
            table_name = table_name_dict[table]
            df_html = df.to_html()
            return render_template('process/info.html', input_part_form=input_part_form, df_html=df_html, table=table, table_name=table_name)
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

    return render_template('process/station.html', table_name_dict=table_name_dict, station=station, station_dict=station_dict)
