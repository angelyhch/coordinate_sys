from flask import url_for, render_template, Blueprint
import pandas as pd
import numpy as np
from coordinate_sys.extensions import cache
from coordinate_sys.process_model import dbo

process_bp = Blueprint('process', __name__, url_prefix='/process')

@process_bp.route('/')
def stations():
    pass
    station_table = dbo.read_table('station')
    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    return render_template('process/stations.html', station_header=station_header, station_list=station_list)


@process_bp.route('/jigs')
def jigs():
    df_jigs = dbo.read_table('jig')
    df_jigs_html = df_jigs.to_html()
    return render_template('process/jigs.html', df_jigs_html=df_jigs_html)


@process_bp.route('/parts') #todo: 各个表格自动识别，用table name 作为参数
def parts():
    df_parts = dbo.read_table('part')
    df_parts_html = df_parts.to_html()
    return render_template('process/parts.html', df_parts_html=df_parts_html)


@process_bp.route('/stations/<station>')
@cache.cached(query_string=True)
def station(station):
    read_table_list = ['jig', 'part']
    station_dict = {}
    for table in read_table_list:
        df_tb = dbo.read_table(table)
        df_tb_st = df_tb.loc[df_tb['station'] == station, ]

        station_dict[table] = df_tb_st

    return render_template('process/station.html', station=station, station_dict=station_dict)
