from flask import url_for, render_template, Blueprint
import pandas as pd
import numpy as np
from coordinate_sys.extensions import cache
from coordinate_sys.process_model import dbo
from coordinate_sys.forms import InputPartForm


process_bp = Blueprint('process', __name__, url_prefix='/process')

info_table_list = ['jig', 'part', 'weldspot', 'tujiao', 'daoruyanzhengjilu']
table_name_dict = {
    'jig': '夹具清单表',
    'part': '零部件清单表',
    'weldspot': '焊点清单表',
    'daoruyanzhengjilu': '车型导入验证记录',
    'tujiao': '涂胶明细表'
}

@process_bp.route('/')
def stations():
    pass
    station_table = dbo.read_table('station')
    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    return render_template('process/stations.html', station_header=station_header, station_list=station_list)


@process_bp.route('/info/<string:url>', methods=['get', 'post'])
def info(url):
    table = url
    input_part_form = InputPartForm()

    if input_part_form.validate_on_submit():
        lingjinahao = input_part_form.lingjianhao.data
        df_pbom = dbo.read_table('pbom')
        df_part = df_pbom.loc[df_pbom['lingjianhao'] == lingjinahao, ]
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
