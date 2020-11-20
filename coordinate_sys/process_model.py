from coordinate_sys.models import engine
from coordinate_sys.extensions import db
import pandas as pd
from coordinate_sys import root_path
import os, sys

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(128))
    line = db.Column(db.String(128))


def manual_input_data_to_station():
    # 设定读取数据源地址
    excel_path = os.path.join(root_path, r"static\process_data_temp", r"station_1108.xlsx")
    # 读取EXCEL数据
    df1 = pd.read_excel(excel_path, header=0, index_col=None)
    # EXCEL数据写入数据库
    df1.to_sql('station', engine, schema='coordinate_data', if_exists='replace') #todo: 以后要和三坐标分析拆分数据库或者拆表

