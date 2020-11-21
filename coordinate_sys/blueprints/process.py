from flask import url_for, render_template, Blueprint
import pandas as pd
import numpy as np
from coordinate_sys.extensions import cache
from coordinate_sys.process_model import dbo

process_bp = Blueprint('process', __name__, url_prefix='/process')

info_table_list = ['jig', 'part', 'weldspot']
table_name_dict = {
    'jig': '夹具清单表',
    'part': '零部件清单表',
    'weldspot': '焊点清单表'
}

@process_bp.route('/')
def stations():
    pass
    station_table = dbo.read_table('station')
    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    return render_template('process/stations.html', station_header=station_header, station_list=station_list)


@process_bp.route('/info/<string:url>')
def daohang(url):
    table = url
    if table in info_table_list:
        df = dbo.read_table(table)
        table_name = table_name_dict[table]
        df_html = df.to_html()
        return render_template('process/daohang.html', df_html=df_html, table_name=table_name)
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

    return render_template('process/station.html', station=station, station_dict=station_dict)
