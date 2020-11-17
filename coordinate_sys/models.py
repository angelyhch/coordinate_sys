import pandas as pd
import json
import os
from numpy import mean
import pygal
from flask import Response
from coordinate_sys.extensions import db, root_path


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
        rel_file = 'static\\data_temp'

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



    # 转换为偏差值
    df_40 = df_3.copy()
    for colname in df_40.columns:
        if colname.startswith('LNB'):
            df_40.loc[:, colname] -= df_40.loc[:, '名义值']
    df_4 = df_40.copy()

    point_name_dict = read_point_name()
    df_4.insert(2, '测点功能', df_4['特征点号'])
    df_4['测点功能'] = [point_name_dict.get(x[:6], '未查到') for x in list(df_4['特征点号'])]
    df = df_4
    return df


def write_point_name(file_path=None):
    if file_path is None:
        file_path = get_file_path()

    df1 = pd.read_excel(file_path, sheet_name=list(range(5, 40)), header=5)
    point_name_dict = {}
    for df in df1:
        df_t1 = df1[df]
        df_t2 = df_t1.loc[:, ['编号 Laber', '功能     Function']]
        df_t3 = df_t2.dropna()
        df_t3.columns = ['测点编号', '测点功能']
        df_dict = dict(zip([x[:6] for x in df_t3['测点编号'] if len(x) == 7], df_t3['测点功能']))
        point_name_dict.update(df_dict)

    point_name_dict_json_dir = os.path.join(root_path, 'static\\point_name_dict.json')

    with open(point_name_dict_json_dir, 'w', encoding='utf8') as f:
        json.dump(point_name_dict, f)

    return point_name_dict

def read_point_name(filepath=None):
    if filepath is None:
        filepath = os.path.join(root_path, 'static\\point_name_dict.json')
    with open(filepath, 'r', encoding='utf8') as f:
        point_name_dict = json.load(f)

    return point_name_dict


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
    del select_points1['测点功能']

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


def warning_point(header_cols=4, new_cols=3, old_cols=9):
    df = read_database()
    cols = df.columns
    df.columns = list(cols[:header_cols]) + [x[:17][-6:] for x in cols[header_cols:]]
    # 近new_cols台 与前old_cols台数据比较
    df['warn'] = df.apply(
        lambda x: int(x[header_cols] < min(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])) +
                  int(x[header_cols] > max(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])) +
                  int(x[header_cols+1] < min(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])) +
                  int(x[header_cols+1] > max(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])) +
                  int(x[header_cols+2] < min(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])) +
                  int(x[header_cols+2] > max(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)]))\
                    , axis=1)
    df_warn1 = df[df['warn'] == 3]
    # 近new_cols台均值与前old_cols台均值差异
    df_warn1['sort_col'] = df_warn1.apply(lambda x: abs(mean(x[header_cols:(header_cols+new_cols)]) - mean(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)])), axis=1)
    df_warn1['均值差异'] = df_warn1.apply(lambda x: mean(x[header_cols:(header_cols+new_cols)]) - mean(x[(header_cols+new_cols):(header_cols+new_cols+old_cols)]), axis=1)
    df_warn2 = df_warn1.sort_values(by=['sort_col'], ascending=False)

    temp = df_warn2.pop('均值差异')
    df_warn2.insert(2, '均值差异', temp)
    df_warn = df_warn2.iloc[:, :(header_cols + new_cols + old_cols)]
    df_warn = df_warn.round(2)
    return df_warn


# if __name__ == '__main__':
#     df_sl = point_select(read_database())
#     resp = chart_select_point(df_sl)
