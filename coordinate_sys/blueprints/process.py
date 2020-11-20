from flask import url_for, render_template, Blueprint
import pandas as pd
import numpy as np
from coordinate_sys.models import engine

process_bp = Blueprint('process', __name__, url_prefix='/process')

@process_bp.route('/')
def stations():
    pass
    station_table = pd.read_sql_table('station', engine)

    station_header = list(station_table)
    station_list = np.array(station_table).tolist()

    #页尾展示工位清单
    station_table_html = station_table.to_html()
    return render_template('process/stations.html', station_header=station_header, station_list=station_list, station_table_html=station_table_html)


@process_bp.route('/stations/<station>')
def station(station):
    pass

    return f'<h2>单个station展示，{station}工位</h2>'