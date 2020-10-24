import pandas as pd
import os
import matplotlib.pyplot as plt
from numpy import mean
import pygal
from flask import Response
from coordinate_sys.extensions import db

try:
    from coordinate_sys import root_path
    temp_rt = 'auto'
except:
    root_path = 'D:\\python\\coordinate_sys\\coordinate_sys'
    temp_rt = 'manual'

try:
    engine = db.engine
except:
    from sqlalchemy import create_engine, inspect
    engine = create_engine('mysql+pymysql://coordinate:coordinate_data@127.0.0.1:3306/coordinate_data')

db_inspector = inspect(engine)

# logger.info(temp_rt)


def get_file_path(file_dir=None):
    '''
    在static文件自动查找data数据地址
    :param file_dir:
    :return:
    '''
    if file_dir is None:
        rel_file = 'static\\coordinate_datas'

    full_file_dir = os.path.join(root_path, rel_file)

    file_list = list(os.walk(full_file_dir))[0][2]
    excel_file = [x for x in file_list if (x[-4:] == 'xlsx') | (x[-4:] == 'xlsm')][0]

    file_path = os.path.join(full_file_dir, excel_file)
    return file_path

def read_excel_data(
        file_path=None,
        header=5,
        usecols=None):
    '''
    读取excel数据,加工成需求的dataframe，
    列名【特征点号，方向，名义值，VIN号】
    行按点号显示
    数据按偏差值
    '''

    if file_path is None:
        file_path = get_file_path()

    if usecols is None:
        usecols = list(range(0, 3)) + list(range(104, 204))

    df_0 = pd.read_excel(file_path, sheet_name='Data', header=header,
                         index_col=None, usecols=usecols)
    # 删除多余4行
    df_1 = df_0.drop(labels=[0, 1, 2, 3])

    # 前三列重命名
    df_2 = df_1.rename(columns={df_1.columns[0]: '特征点号',
                                df_1.columns[1]: '方向',
                                df_1.columns[2]: '名义值'})

    # 筛选出有效数据
    df_3 = df_2[df_2['方向'].isin(['X', 'Y', 'Z'])]

    # 补全点号
    df_3.loc[:'特征点号'].fillna(method='ffill', limit=2, axis=0, inplace=True)

    '''
        前几列的列名无法去掉.1 。
        for colname in df_40.columns:
            if colname.endswith('.1'):
                df_40.rename(columns={colname: colname[:-2]})
    '''

    # 转换为偏差值
    df_40 = df_3
    for colname in df_40.columns:
        if colname.startswith('LNB'):
            df_40.loc[:, colname] -= df_40.loc[:, '名义值']
    df_4 = df_40

    # 设置小数点位数

    df = df_4
    return df


def read_point_name(file_path=None):
    if file_path is None:
        file_path = get_file_path()

    df1 = pd.read_excel(file_path, sheet_name=list(range(5, 40)), header=5)
    point_name_dict = {}
    for df in df1:
        df_t1 = df1[df]
        df_t2 = df_t1.loc[:, ['编号 Laber', '功能     Function']]
        df_t3 = df_t2.dropna()
        df_t3.columns = ['测点编号', '测点功能']
        # df_t3['测点查询号'] = df_t3.apply(lambda x: x[0][:6], axis=1)
        # df_t3.pop('测点编号')
        df_dict = dict(zip([x[:6] for x in df_t3['测点编号'] if len(x) == 7], df_t3['测点功能']))
        point_name_dict.update(df_dict)

    return point_name_dict  #todo:待调试



def refresh_database(df):
    df.to_sql('coordtemp', engine, schema='coordinate_data', if_exists='replace')


def read_database():
    try:
        df_read = pd.read_sql_table('coordtemp', engine, index_col='index')
    except:
        df = read_excel_data()
        df.to_sql('coordtemp', engine, schema='coordinate_data', if_exists='replace')
        df_read = pd.read_sql_table('coordtemp', engine, index_col='index')
    return df_read



def point_select(df_readsql, point_list=None, direction='X', vin_list=None):
    '''
    按照点号，方向，vin 清单，查询出数据
    :param df_readsql:
    :param point_list:
    :param direction:
    :param vin_list:
    :return:
    '''

    if point_list is None:
        point_list = ['KN0001L', 'KN0002L', 'KN0003L']
    if vin_list is None:
        vin_list = ['特征点号', '方向', '名义值'] + ['LNBMCUAK1LT108228', 'LNBMCUAKXLT107904', 'LNBMCUAK5LT106417',
                                            'LNBMCUAK2LT106164', 'LNBMCUAK0LT106096', 'LNBMCUAK9LT105982',
                                            'LNBMCUAK4LT104514']

    cols = df_readsql.columns
    df0 = df_readsql
    df1 = df0.loc[(df0[cols[0]].isin(point_list)) & (df0[cols[1]] == direction), vin_list]

    df = df1
    return df


def chart_select_point(select_points_df):
    '''
    绘图
    :return:
    '''
    select_points1 = select_points_df
    select_points1['特征点号'] = select_points1['特征点号'].map(str) + select_points1['方向'].map(str)
    del select_points1['方向']
    del select_points1['名义值']

    select_points2 = select_points1.set_index('特征点号')
    select_points = select_points2.round(2)
    chart_data = select_points.transpose()

    chart_xlabel_list1 = chart_data.index.to_list()  # todo: xlabel 改成6位 短 vin号
    chart_xlabel_list = [x[0:17][-6:] for x in chart_xlabel_list1]

    # pygal svg图生成
    chart_pygal = pygal.Line(x_label_rotation=-90)
    chart_pygal.x_labels = chart_xlabel_list

    for p in chart_data.columns.to_list():
        chart_pygal.add(p, chart_data[p])

    return Response(response=chart_pygal.render(), content_type="image/svg+xml")


def warning_point():
    df = read_database()
    cols = df.columns
    df.columns = list(cols[:3]) + [x[:17][-6:] for x in cols[3:]]
    # 近3台 与前9台数据比较
    df['warn'] = df.apply(
        lambda x: int(x[3] < min(x[6:15])) + int(x[3] > max(x[6:15])) + int(x[4] < min(x[6:15])) + int(
            x[4] > max(x[6:15])) + int(x[5] < min(x[6:15])) + int(x[5] > max(x[6:15])), axis=1)
    df_warn1 = df[df['warn'] == 3]
    # 近3台均值与前9台均值差异
    df_warn1['sort_col'] = df_warn1.apply(lambda x: abs(mean(x[3:6]) - mean(x[6:15])), axis=1)
    df_warn1['均值差异'] = df_warn1.apply(lambda x: mean(x[3:6]) - mean(x[6:15]), axis=1)
    df_warn2 = df_warn1.sort_values(by=['sort_col'], ascending=False)
    # 更改sort_col 列位置
    # temp = df_warn2.pop('sort_col')
    # df_warn2.insert(2, 'sort_col', temp)
    # 更改均值差异列位置
    temp = df_warn2.pop('均值差异')
    df_warn2.insert(2, '均值差异', temp)
    df_warn = df_warn2.iloc[:, :17]
    df_warn = df_warn.round(2)
    return df_warn


# if __name__ == '__main__':
#     df_sl = point_select(read_database())
#     resp = chart_select_point(df_sl)
