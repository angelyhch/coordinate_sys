from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from os import walk, getcwd
from math import sqrt
import re


def find_file():
    '''
    找到同文件夹下的xlsx文件（三坐标测量数据‘Data')
    '''

    file_name_list_0 = list((walk(getcwd())))[0][2]
    file_name = [x for x in file_name_list_0 if (x[-4:] == 'xlsx')][0]
    return file_name


def read_data(head_name=None):
    '''
    读取excel数据,加工成需求的dataframe
    '''

    print('开始提取...')
    run_state_text.insert('end', '{}:---开始提取\n'.format(datetime.now()))

    # 从同文件夹下读取xlsx文件
    if head_name is None:
        head_name = ['point_name', 'direction', '名义值', 'degree', 'define_degree',
                     'last1', 'last2', 'last3', 'last4', 'last5', 'last6', 'last7', 'last8',
                     'last9', 'last10']
    df_0 = pd.read_excel(find_file(), sheet_name='Data', header=None,
                         names=head_name, index_col=None, usecols=list(range(0, 15)), skiprows=10)

    # 筛选出有效数据到df_1
    df_1 = df_0[df_0['direction'].isin(['X', 'Y', 'Z'])]
    # print('df_1', df_1)

    # 补全point_name列名称，用fillna方法
    df_1['point_name'].fillna(method='ffill', limit=2, axis=0, inplace=True)

    print('df_1', df_1)
    run_state_text.insert('end', '{}:---数据提取完成\n'.format(datetime.now()))

    return df_1


def chart_display(column_m_name='名义值', column_n_name='last1', plane_choice=1, color_limit_num=0.75,
                  choose_points=None, data_source=None,
                  scatter_m_normal_color='gray', scatter_n_normal_color='yellow', scatter_m_out_color='blue',
                  scatter_n_out_color='red'):
    '''
    可视化数据对比
    '''

    # 显示参数值：
    print('chart_display parameter 参数列表', datetime.now())
    print("column_m_name", column_m_name)
    print('column_n_name', column_n_name)
    print('plane_choice', plane_choice)
    print('color_limit_num', color_limit_num)
    print('choose_point_list', choose_points)
    run_state_text.insert('end', '{}---参数列表：\n第一组数据：{}\n第二组数据：{}\n对边平面选择：{}\n展示范'
                                 '围界限值：{}\n比较测点清单：{}\n'.format(datetime.now(), column_m_name, column_n_name,
                                                               plane_choice,
                                                               color_limit_num, choose_points))

    # 判断参数输入
    if choose_points is None:
        choose_points = 'KN0018L,KN0019L,KN0020L,KN0021R,KN0022L,KN0022R'

    # 字符串去空白符
    choose_points_remove_blank = ''.join(choose_points.replace('\n', '').replace('\r', '').split())
    # 字符串转列表
    choose_point_list = choose_points_remove_blank.split(',')
    print('choose_point_list 对比点清单', choose_point_list)
    run_state_text.insert('end', '{}:---对比点清单列表：{}\n'.format(datetime.now(), choose_point_list))

    error_word_count = 0
    for item in choose_point_list:
        if re.match('\w\w\d\d\d\d\w', item):
            pass
        else:
            print('choose points input error ,对比点输入有错误！---{}'.format(item))
            run_state_text.insert('end', '{}:---对比点输入有错误---{}'.format(datetime.now(), item))
            error_word_count += 1
    if error_word_count != 0:
        print('共发现{}个对比点输入有错误'.format(error_word_count))
        run_state_text.insert('end', '{}:---共发现{}个对比点输入错误\n'.format(datetime.now(), error_word_count))
        return '共发现{}个对比点输入有错误'.format(error_word_count)

    # color_limit_num 偏差界限值
    if 0 <= color_limit_num <= 3:
        pass
    else:
        print('color_limit_num out of rangescope (0,3), 偏差界限设置错误')
        run_state_text.insert('end', '{}:---偏差界限设置错误，偏差值---{}\n'.format(datetime.now(), color_limit_num))
        return 'color_limit_num out of rangescope (0,3), 偏差界限设置错误'

    # 数据导入
    if data_source is None:
        data_df_0 = read_data()
    else:
        data_df_0 = data_source

    # 选择平面方向，判断输入格式
    if plane_choice != 0:
        if plane_choice == 1:
            choose_direction_a = 'X'
            choose_direction_b = 'Y'
        elif plane_choice == 2:
            choose_direction_a = 'Y'
            choose_direction_b = 'Z'
        elif plane_choice == 3:
            choose_direction_a = 'X'
            choose_direction_b = 'Z'
        elif plane_choice == 4:
            choose_direction_a = 'Y'
            choose_direction_b = 'X'
        elif plane_choice == 5:
            choose_direction_a = 'Z'
            choose_direction_b = 'Y'
        elif plane_choice == 6:
            choose_direction_a = 'Z'
            choose_direction_b = 'X'
        else:
            print('plane_choice error,平面选择输入错误!')
            run_state_text.insert('end', '{}---平面选择输入错误\n'.format(datetime.now()))
            return 'plane_choice error,平面选择输入错误!'

        # 筛选出需求数据
        data_df_1 = data_df_0[data_df_0['point_name'].isin(choose_point_list)]

        print('data_df_1', data_df_1)
        run_state_text.insert('end', '{}---测定数据加工结果:\n {}'.
                              format(datetime.now(), data_df_1.loc[:, ['point_name', column_m_name, column_n_name]]))


        plt_list_m_x_0 = data_df_1[column_m_name][data_df_1['direction'] == choose_direction_a]
        plt_list_n_x_0 = data_df_1[column_n_name][data_df_1['direction'] == choose_direction_a]
        plt_list_m_y_0 = data_df_1[column_m_name][data_df_1['direction'] == choose_direction_b]
        plt_list_n_y_0 = data_df_1[column_n_name][data_df_1['direction'] == choose_direction_b]

        print('单平面对比列数据加工完成', datetime.now())
        run_state_text.insert('end', '{}---单平面对比数据加工完成\n'.format(datetime.now()))
        # 数据转化成列表list
        plt_list_m_a_1 = list(plt_list_m_x_0)
        plt_list_m_b_1 = list(plt_list_m_y_0)
        plt_list_n_a_1 = list(plt_list_n_x_0)
        plt_list_n_b_1 = list(plt_list_n_y_0)

        # 测点清单
        plt_point_list = list(data_df_1['point_name'])[0::3]
        run_state_text.insert('end', '{}---显示测点清单{}'.format(datetime.now(), plt_point_list))

        # 对应点偏差值计算
        distance_a_0 = [i[0] - i[1] for i in list(zip(plt_list_n_a_1, plt_list_m_a_1))]
        distance_b_0 = [i[0] - i[1] for i in list(zip(plt_list_n_b_1, plt_list_m_b_1))]
        distance_abs_0 = [sqrt(i[0] ** 2 + i[1] ** 2) for i in list(zip(distance_a_0, distance_b_0))]

        # 散点大小设置
        size_value_list = [i * 200 for i in distance_abs_0]

        # 散点颜色设置
        color_value_list_m = [
            scatter_m_normal_color * (color_limit_num > i) + scatter_m_out_color * (color_limit_num <= i)
            for i in distance_abs_0]
        color_value_list_n = [
            scatter_n_normal_color * (color_limit_num > i) + scatter_n_out_color * (color_limit_num <= i)
            for i in distance_abs_0]

        # 图表展示
        plt.scatter(plt_list_m_a_1, plt_list_m_b_1, marker='s', s=size_value_list, c=color_value_list_m, label='first')
        plt.scatter(plt_list_n_a_1, plt_list_n_b_1, marker='s', s=size_value_list, c=color_value_list_n, label='second')

        for xy in zip(distance_a_0, distance_b_0, plt_list_m_a_1, plt_list_m_b_1, distance_abs_0, plt_point_list):
            plt.annotate('%s\n%0.1f,%0.1f' % (xy[5], xy[0], xy[1]) * (xy[4] > color_limit_num), xy=(xy[2], xy[3]),
                         xytext=(-20, 10), textcoords='offset points')

        print('time chart scatter display', datetime.now())
        run_state_text.insert('end', '{}---单平面数据展示绘图完成\n\n\n'.format(datetime.now()))
        plt.title('%s-%s View Chart' % (choose_direction_a, choose_direction_b))
        plt.xlabel(choose_direction_a)
        plt.ylabel(choose_direction_b)
        plt.grid()
        plt.show()

    else:
        pass

        # 筛选出需求数据

        plt_list_m_x_0 = data_df_0[column_m_name][data_df_0['direction'] == 'X'][
            data_df_0['point_name'].isin(choose_point_list)]
        plt_list_m_y_0 = data_df_0[column_m_name][data_df_0['direction'] == 'Y'][
            data_df_0['point_name'].isin(choose_point_list)]
        plt_list_m_z_0 = data_df_0[column_m_name][data_df_0['direction'] == 'Z'][
            data_df_0['point_name'].isin(choose_point_list)]

        plt_list_n_x_0 = data_df_0[column_n_name][data_df_0['direction'] == 'X'][
            data_df_0['point_name'].isin(choose_point_list)]
        plt_list_n_y_0 = data_df_0[column_n_name][data_df_0['direction'] == 'Y'][
            data_df_0['point_name'].isin(choose_point_list)]
        plt_list_n_z_0 = data_df_0[column_n_name][data_df_0['direction'] == 'Z'][
            data_df_0['point_name'].isin(choose_point_list)]

        print('time 对比列数据抽取', datetime.now())
        run_state_text.insert('end', '{}---多维度对比数据抽取完成\n'.format(datetime.now()))
        # 数据转化成列表list
        plt_list_m_x_1 = list(plt_list_m_x_0)
        plt_list_m_y_1 = list(plt_list_m_y_0)
        plt_list_m_z_1 = list(plt_list_m_z_0)
        plt_list_n_x_1 = list(plt_list_n_x_0)
        plt_list_n_y_1 = list(plt_list_n_y_0)
        plt_list_n_z_1 = list(plt_list_n_z_0)

        def subplot_show(plt_list_m_a, plt_list_m_b, plt_list_n_a, plt_list_n_b):

            # 对应点偏差值计算
            distance_a = [i[0] - i[1] for i in list(zip(plt_list_m_a, plt_list_n_a))]
            distance_b = [i[0] - i[1] for i in list(zip(plt_list_m_b, plt_list_n_b))]
            distance_abs = [sqrt(i[0] ** 2 + i[1] ** 2) for i in list(zip(distance_a, distance_b))]

            # 散点大小设置
            size_value_list = [i * 200 for i in distance_abs]

            # 散点颜色设置
            color_value_list_m = [
                scatter_m_normal_color * (color_limit_num > i) + scatter_m_out_color * (color_limit_num <= i)
                for i in distance_abs]
            color_value_list_n = [
                scatter_n_normal_color * (color_limit_num > i) + scatter_n_out_color * (color_limit_num <= i)
                for i in distance_abs]

            # 图表展示
            plt.scatter(plt_list_m_a, plt_list_m_b, marker='s', s=size_value_list, c=color_value_list_m,
                        label='first')
            plt.scatter(plt_list_n_a, plt_list_n_b, marker='s', s=size_value_list, c=color_value_list_n,
                        label='second')

        # 左上图, xz图
        plt.subplot(221)
        subplot_show(plt_list_m_x_1, plt_list_m_z_1, plt_list_n_x_1, plt_list_n_z_1)
        plt.xlabel('x')
        plt.ylabel('z')

        # 右上图, yz图
        plt.subplot(222)
        subplot_show(plt_list_m_y_1, plt_list_m_z_1, plt_list_n_y_1, plt_list_n_z_1)
        plt.xlabel('y')
        plt.ylabel('z')

        # 左下图, xy图
        plt.subplot(223)
        subplot_show(plt_list_m_x_1, plt_list_m_y_1, plt_list_n_x_1, plt_list_n_y_1)
        plt.xlabel('x')
        plt.ylabel('y')

        # 右下图, yx图
        plt.subplot(224)
        subplot_show(plt_list_m_y_1, plt_list_m_x_1, plt_list_n_y_1, plt_list_n_x_1)
        plt.xlabel('y')
        plt.ylabel('x')

        run_state_text.insert('end', '{}---多维度数据展示绘图完成\n\n\n'.format(datetime.now()))
        plt.grid()
        plt.show()


def _test():
    import doctest
    doctest.testmod(verbose=True)


def select_points_dict():
    '''
    输入备选测点清单
    '''

    select_points_dict = {}
    # 左右轮罩相关点，含滑柱安装孔
    select_points_dict[
        'c53f_Zuoyoulunzhao_Qainhuazhu_p_02'] = 'KH0017L,KH0015L,KH0016L,KH0015R,KH0016R,KH0017R,KN0002L,' \
                                                'KN0002R,KN0003L,KN0003R,GN0004L,GN0005L,GN0004R,GN0005R'
    # 发动机悬置安装点
    select_points_dict['c53f_Fadongjixuanzhi_p_02'] = 'KN0018L,KN0019L,KN0020L,KN0021R,KN0022L,KN0022R'

    # 空气室相关点，总成定位，发盖铰链安装
    select_points_dict[
        'c53f_KongqishiFadongjigai_p_02_03'] = 'KN0013L,KN0014L,KN0013R,KN0014R,KH0024L,KH0025R,GN0026L,GN0027L'

    # 前副车架总成定位点
    select_points_dict['c53f_Qianfuchejia_p_03'] = 'KP0046L,KP0046R,KN0047L,KN0047R,KN0048L,KN0048R'

    # 前地板测量点
    select_points_dict[
        'c53f_Qiandiban_p_05_06'] = 'GN1003L,GN1004L,GN1005L,GN1005R,GN1006LGN1007L,GP1008R,GP1009R,GN1010L,GN1010R,' \
                                    'GN1011L,GN1011R,KH1012L,KH1013L,KH1013R,KN1014L,KN1014R,KN1015L,KN1015R,KH1016L,' \
                                    'KH1016R,KH1017L,KH1017R,GH1018L,GH1018R,GH1019L,GH1019R,GH1020L,GH1020R,GH1021L,' \
                                    'GH1021R,EH1024L,EH1025L,EH1024R,EH1025R'

    # 后副车架安装点相关，后地板
    select_points_dict[
        'c53f_HoudibanHoufuchejia_p_07_08'] = 'KN2016L,KN2017L,KN2018L,KS2019L,KP2020L,KN2016R,KN2017R,KN2018R,' \
                                              'KS2019R,KP2020R,EH2002L,EH2004R,GH2003L,GH2003R,KH2025L,KH2025R,' \
                                              'EH2026L,EH2026R,EH2027L,EH2027R,EH2028L '

    # 前段模块安装板
    select_points_dict[
        'c53f_Qianduanmokuai_p_02'] = 'GH0008L,GH0008R,KN0009L,KN0009R,KN0010L,KN0010R,KN0011L,KN0011R,KN0012L,KN0012R'

    # 四门铰链，A柱下板，侧围柱定位孔 左侧
    select_points_dict[
        'c53f_Simenjiaolian_Azhuxiaban_L_p_09'] = 'KH3001L,KN3003L,KN3004L,KN3005L,' \
                                                'GH3006L,GN3007L,GN3008L,GN3009L,GN3010L,' \
                                                'KH3011L,KN3012L,KN3013L,KN3014L,' \
                                                'KH3016L'

    # 四门铰链，A柱下板，侧围柱定位孔 右侧
    select_points_dict[
        'c53f_Simenjiaolian_Azhuxiaban_R_p_09'] = 'KH3001R,KN3003R,KN3004R,KN3005R,' \
                                                  'GN3007R,GN3008R,GN3009R,' \
                                                  'GN3010R,KH3011R,KN3012R,KN3013R,' \
                                                  'KN3014R,KH3016R'

 # C53F 备选数据清单输入
    # 左右轮罩相关点
    select_points_dict[
        'c53f_Zuoyoulunzhao_p_01'] = 'KN0002L,KN0002R,KN0003L,KN0003R,GN0004L,GN0004R,GN0005L,GN0005R,KN0006L,' \
                                      'KN0006R,KN0007L,KN0007R,KH0015L,KH0015R,KH0016L,KH0016R,KH0017L,KH0017R ,KN0019L,KN0022R'

    # 空气室相关点
    select_points_dict[
        'c53f_Kongqishi_p_01'] = 'KN0001L,KN0001R,KN0013L,KN0013R,KN0014L,KN0014R,KH0024L,KH0025R,GN0026L,GN0027L'

    # 悬置总成安装螺母
    select_points_dict[
        'c53f_Qianzongliangxuanzhizongcheng_p_01'] = 'KN0018L,KN0019L,KN0020L,KN0021R.KN0022R,KN0023R'

    # 前副车架
    select_points_dict[
        'c53f_Qianzongliangqianfuchejian_p_02'] = 'KP0046L,KP0046R,KN0047L,KN0047R,KN0048L,KN0048R'

    # 前端模块安装板
    select_points_dict[
        'c53f_Qianduanmokuaianzhuangban_p_01'] = 'GH0008L,GH0008R,KN0009L,KN0009R,KN0010L,KN0010R,KN0011L,KN0011R,' \
                                                  'KN0012L,KN0012R, GH0070L,GH0070R,GH0071L,GH0071R'

    # 仪表板横梁安装点
    select_points_dict['c53f_Yibiaobanhengliang_p_02'] = 'KH0028L,KH0028R,KN0029L,KN0029R,KN0030L,KN0030R'

    # 前座椅安装相关点
    select_points_dict[
        'c53f_Zuoyianzhuang_p_04'] = 'KH1012L,KH1012R,KH1013L,KH1013R,KN1014L,KH1014R,KN1015L,KH1015R,KN1016L,KH1016R,KH1017L,KN1017R,' 
                                         

    # 中通道相关
    select_points_dict[
        'c53f_Zhongtongdao_p_04'] = 'GN1001L,GN1001R,GN1002L,GN1002R,GN1003L,GN1004L,GP1005L,GP1005R,GP1006L,GP1007L,GP1008R,GP1009R,GN1010L,GN1010R,' \
                                     'GN1011L,GN1011R,GN1026R,GN1027R '


    # 前地板侧边梁
    select_points_dict[
        'c53f_Qiandibancebianliang_p_05'] = 'GH1018L,GH1018R,GH1019L,GH1019R,GH1020L,GH1020R,GH1021L,GH1021R,' 
                                             
                                             

    # 前地板面板定位孔
    select_points_dict['c53f_Mianbandingweikong_p_05'] = 'EH1024L,EH1024R,EH1025L,EH1025R'

    # 后地板面板定位孔
    select_points_dict['c53f_Houdianbanmianbandingweikong_p_06'] = 'EH2026L,EH2026R,EH2027L,EH2027R,EH2028L,EH2028R'

    # 后地板总装安装点
    select_points_dict[
        'c53f_Putonganzhuangdian_p_06'] = 'EH2004R,EH2002L,GH2003L,GH2003R,GN2005L,GN2005R,GN2006L,GN2006R,GN2007L,GN2007R,' \
                                           'GN2008L,GN2008R,'

    # 后围板点
    select_points_dict[
        'c53f_Houweiban_p_06'] = 'EH3044L,EH3044R,GN2013R,GN2012R,GP2011C,GS2010L,,GS2010R,GS2009L,GS2009R,GH2014L,GH2014R,' \
                                  'GH2015L,GH2015R '

    # 总装吊具定位孔
    select_points_dict['c53f_Zongzhuangdiaojudingwei_p_07'] = 'KH2025L,KH2025R'
    

    # 后副车架
    select_points_dict[
        'c53f_Houfuchejian_p_07'] = 'KN2017L,KN2017R,KN2016L,KN2016R,KN2018L,KN2018R,KS2019L,KS2019R,KP2020L,KP2020R'
    
   

    # 侧围A柱下板L
    select_points_dict[
        'c53f_Azhu_L_p_08'] = 'KH3001L,KN3002L,KN3003L,KN3004L,KN3005L,GH3006L,GN3007L,GN3008L,GN3009L,GN3010L'

    # 侧围A柱下板R
    select_points_dict[
        'c53f_Azhu_R_p_08'] = 'KH3001R,KN3002R,KN3003R,KN3004R,KN3005R,GN3007R,GN3008R,GN3009R,GN3010R'

    # 侧围总成定位孔
    select_points_dict['c53f_Ceweizongchengdingweikong_p_08'] = 'KH3001L,KH3001R,KH3016L,KH3016R'

    # 四门铰链L
    select_points_dict[
        'c53f_Simenjiaolian_L_p_08'] = 'KN3002L,KN3003L,KN3004L,KN3005L,KH3011L,KN3012L,KN3013L,KN3014L,KN3015L'

    # 四门铰链R
    select_points_dict[
        'c53f_SimenjiaoRian_R_p_08'] = 'KN3002R,KN3003R,KN3004R,KN3005R,KH3011R,KN3012R,KN3013R,KN3014R,KN3015R'

    # 四门锁环限位器L
    select_points_dict['c53f_SimenSuohuanXianweiqi_L_p_08'] = 'GN3017L,GN3018L,GN3019L,GN3020L,GN3021L,GN3022L'

    # 四门锁环限位器R
    select_points_dict['c53f_SimenSuohuanXianweiqi_R_p_08'] = 'GN3017R,GN3018R,GN3019R,GN3020R,GN3021R,GN3022R'


    # 后三角窗L
    select_points_dict['c53f_Housanjiaochuang_L_p_09'] = 'GH3023L,GH3024L,GH3025L'

    # 后三角窗R
    select_points_dict['c53f_Housanjiaochuang_R_p_09'] = 'GH3023R,GH3024R,GH3025R'

    # 后保支架L
    select_points_dict['c53f_Houbaozhijia_L_p_10'] = 'KH3026L,KH3027L,KH3028L,KH3029L,KH3030L,KH3031L,KH3032L'

    # 后保支架R
    select_points_dict['c53f_Houbaozhijia_R_p_10'] = 'KH3026R,KH3027R,KH3028R,KH3029R,KH3030R,KH3031R,KH3032R'

    # 尾灯盒L
    select_points_dict[
        'c53f_Weidenghe_L_p_10'] = 'KH3033L,KH3034L,KH3035L,KH3036L,KH3037L,KH3038L,KH3039L,KH3040L,KH3041L,KH3042L,' \
                                    'KH3043L '

    # 尾灯盒R
    select_points_dict[
        'c53f_Weidenghe_R_p_10'] = 'KH3033R,KH3034R,KH3035R,KH3036R,KH3037R,KH3038R,KH3039R,KH3040R,KH3041R,KH3042R,' \
                                    'KH3043R '

    # 后防撞梁安装
    select_points_dict[
        'c53f_Houfangzhuangliang_p_10'] = 'EH3044L,EH3044R,GP3045L,GP3045R,GP3046L,GP3046R.GP3047L,GP3047R'

    # 后减震器L
    select_points_dict['c53f_Houjianzhenqi_L_p_11'] = 'KN3048L,KN3049L,KN3050L'

    # 后减震器R
    select_points_dict['c53f_Houjianzhenqi_R_p_11'] = 'KN3048R,KN3049R,KN3050R'

    # 油箱口
    select_points_dict['c53f_Manchongzuo_p_11'] = 'GH3051R,GH3052R,GH3053R,GH3054R,GH3055R,GN3056R,GN3057R'

    # A柱 内板L
    select_points_dict[
        'c53f_Azhuneiban_p_12'] = 'GH3058L,GH3059L,GH3060L,GN3061L,KH3064L,GH3065L,GH3066L'

    # A柱 内板R
    select_points_dict[
        'c53f_Azhuneiban_p_12'] = 'GH3058R,GH3059R,GH3060R,GN3061R,GN3062R,GN3063R,GH3065R,GH3066R'

    # B柱内板L
    select_points_dict[
        'c53f_Bzhuneiban_p_12'] = 'GH3067L,GH3068L,GH3069L,GH3070L,GH3071L,GH3072L,GH3073L,GH3074L,GH3075L'

    # B柱内板R
    select_points_dict['c53f_Bzhuneiban_p_12'] = 'GH3067R,GH3068R,GH3069R,GH3070R,GH3071R,GH3072R,GH3073R,GH3074R,GH3075R'

    # C 柱内板L
    select_points_dict['c53f_Czhuneiban_p_12'] = 'GH3076L,GH3077L,GH3078L,GH3079L,GH3080L,GH3081L,GH3082L'

    # C 柱内板R
    select_points_dict['c53f_Czhuneiban_p_12'] = 'GH3076R,GH3077R,GH3078R,GH3079R,GH3080R,GH3081R,GH3082R'

    # 后隔板
    select_points_dict['c53f_Hougeban_p_13'] = 'EH3083L,EH3084R,GH3085L,GH3085R,CH3086C,GH3087L,GH3087R'

    # 行李箱铰链
    select_points_dict['c53f_Xinglixiangjiaolian_p_13'] = 'KH3088L,KH3088R,KH3089L,KH3089R,KH3090L,KH3090R'

    # 后排座椅及衣帽架
    select_points_dict[
        'c53f_HouzuoyiYimaojia_p_13'] = 'GH3092L,GH3092R,GH3093L,GH3093R,GH3094L,GH3095L,GH3096R,GN3097L,GN3097R,' \
                                         'KH3098L,KH3099L,KH3099R '

    # 顶棚前横梁
    select_points_dict[
        'c53f_DingpengQianhengliang_p_22'] = 'EH4001L,EH4002R,GH4003L,GH4003R,GH4004L,GH4005R'

    # 顶棚后横梁
    select_points_dict['c53f_DingpengHouhengliang_p_22'] = 'EH4006L,EH4007R,GH4008L,GH4008R,GH4009C'

    # 天窗
    select_points_dict[
        'c53f_Tianchuang_p_22'] = 'KH4010R,KH4011R,KH4012L,KH4012R,KN4013C,KN4014L,KN4014R,KN4015L,KN4015R,KN4016L,' \
                                   'KN4016R,KN4017L,KN4017R,KN4018L,KN4018R,KN4019L,KN4019R,KN4020L,KN4020R '








    # C53FB 备选数据清单输入
    # 左右轮罩相关点
    select_points_dict[
        'c53fb_Zuoyoulunzhao_p_01'] = 'KN0002L,KN0002R,KN0003L,KN0003R,GN0004L,GN0004R,GN0005L,GN0005R,KN0006L,' \
                                      'KN0006R,KN0007L,KN0007R,KH0015L,KH0015R,KH0016L,KH0016R,KH0017L,KH0017R '

    # 空气室相关点
    select_points_dict[
        'c53fb_Kongqishi_p_01'] = 'KN0001L,KN0001R,KN0013L,KN0013R,KN0014L,KN0014R,KH0026L,KH0027R,GN0028L,GN0029L'

    # 悬置总成安装螺母
    select_points_dict[
        'c53fb_Qianzongliangxuanzhizongcheng_p_01'] = 'KN0018L,KN0019L,KN0020L,KN0021.KN0022R,KN0023R,KN0024R,KN0025R'

    # 前副车架
    select_points_dict[
        'c53fb_Qianzongliangqianfuchejian_p_02'] = 'KP0044L,KP0044R,KN0045L,KN0045R,KN0046L,KN0046R'

    # 前端模块安装板
    select_points_dict[
        'c53fb_Qianduanmokuaianzhuangban_p_01'] = 'GH0008L,GH0008R,KP0009L,KP0009R,KN0010L,KN0010R,KN0011L,KN0011R,' \
                                                  'KN0012L,KN0012R, '

    # 仪表板横梁安装点
    select_points_dict['c53fb_Yibiaobanhengliang_p_02'] = 'KH0030L,KH0030R,KN0031L,KN0031R,KN0032L,KN0032R'

    # 前座椅安装相关点
    select_points_dict[
        'c53fb_Zuoyianzhuang_p_04'] = 'KH1012L,KH1013L,KN1017L,KN1016L,KN1014L,KN1015L,KH1014R,KH1015R,KN1018R,' \
                                          'KN1019R,KN1020R,KN1021R '

    # 中通道相关
    select_points_dict[
        'c53fb_Zhongtongdao_p_04'] = 'GN1003L,GN1026R,GN1004L,GN1027R,GP1005L,GP1005R,GP1008R,GN1005L,GN1006L,' \
                                     'GP1007L,GP1007R '


    # 前地板侧边梁
    select_points_dict[
        'c53fb_Qiandibancebianliang_p_05'] = 'GH1018L,GH1018R,GH1019L,GH1019R,GH1020L,GH1020R,GH1021L,GH1021R,' \
                                             'GH1028L,GH1028R '

    # 前地板面板定位孔
    select_points_dict['c53fb_Mianbandingweikong_p_05'] = 'EH1024L,EH1024R,EH1025L,EH1025R'

    # 后地板面板定位孔
    select_points_dict['c53fb_Houdianbanmianbandingweikong_p_06'] = 'EH2026L,EH2026R,EH2027L,EH2027R,EH2028L,EH2028R'

    # 后地板总装安装点
    select_points_dict[
        'c53fb_Putonganzhuangdian_p_06'] = 'EH2004R,EH2002L,GH2003L,GH2003R,GN2005L,GN2005R,GP2006L,GP2006R,GN2008L,' \
                                           'GN2008R,GN2007L,GN2007R '

    # 后围板点
    select_points_dict[
        'c53fb_Houweiban_p_06'] = 'GN2013R,GN2012R,GP2011C,GS2010L,GS2010L,GS2010R,GS2009L,GS2009R,GH2014L,GH2014R,' \
                                  'GH2015L,GH2015R '

    # 总装吊具定位孔
    select_points_dict['c53fb_Zongzhuangdiaojudingwei_p_07'] = 'KH2030L,KH2030R,KH2025L,KH2025R'

    # 电池安装螺母
    select_points_dict[
        'c53fb_Dianchianzhuang_p_07'] = 'KN2031L,KN2031R,KN2032L,KN2032R,KN2033L,KN2033R,KN2034L,KN2034R,KN2035L,' \
                                        'KN2035R,KN2036L,KN2036R,KN2037L,KN2037R,KN2038L,KN2038R,KN2039L,KN2039R,' \
                                        'KN2040L,KN2040R,KN2040L,KN2040R'

    # 后副车架
    select_points_dict[
        'c53fb_Houfuchejian_p_07'] = 'KN2017L,KN2017R,KN2016L,KN2016R,KN2018L,KN2018R,KS2019L,KS2019R,KP2020L,KP2020R'

    # 侧围A柱下板L
    select_points_dict[
        'c53fb_Azhu_L_p_08'] = 'KH3001L,KN3002L,KN3003L,KN3004L,KN3005L,GH3006L,GN3007L,GN3008L,GN3009L,GN3010L'

    # 侧围A柱下板R
    select_points_dict[
        'c53fb_Azhu_R_p_08'] = 'KH3001R,KN3002R,KN3003R,KN3004R,KN3005R,GN3007R,GN3008R,GN3009R,GN3010R'

    # 侧围总成定位孔
    select_points_dict['c53fb_Ceweizongchengdingweikong_p_08'] = 'KH3001L,KH3001R,KH3016L,KH3016R'

    # 四门铰链L
    select_points_dict[
        'c53fb_Simenjiaolian_L_p_08'] = 'KN3002L,KN3003L,KN3004L,KN3005L,KN3011L,KN3012L,KN3013L,KN3014L,KN3015L'

    # 四门铰链R
    select_points_dict[
        'c53fb_SimenjiaoRian_R_p_08'] = 'KN3002R,KN3003R,KN3004R,KN3005R,KN3011R,KN3012R,KN3013R,KN3014R,KN3015R'

    # 四门锁环限位器L
    select_points_dict['c53fb_SimenSuohuanXianweiqi_L_p_08'] = 'GN3017L,GN3018L,GN3019L,GN3020L,GN3021L,GN3022L'

    # 四门锁环限位器R
    select_points_dict['c53fb_SimenSuohuanXianweiqi_R_p_08'] = 'GN3017R,GN3018R,GN3019R,GN3020R,GN3021R,GN3022R'

    # 下饰板安装孔L
    select_points_dict[
        'c53fb_Xiashiban_p_09'] = 'GH3269L,GH3270L,GH3280L,GH3281L,GH3282L,GH3283L,GH3284L,GH3285L,GH3286L,GH3287L,' \
                                  'GH3288L,GH3289L '

    # 下饰板安装孔R
    select_points_dict[
        'c53fb_Xiashiban_p_09'] = 'GH3269R,GH3270R,GH3280R,GH3281R,GH3282R,GH3283R,GH3284R,GH3285R,GH3286R,GH3287R,' \
                                  'GH3288R,GH3289R '

    # 后三角窗L
    select_points_dict['c53fb_Housanjiaochuang_L_p_09'] = 'GH3023L,GH3024L,GH3025L'

    # 后三角窗R
    select_points_dict['c53fb_Housanjiaochuang_R_p_09'] = 'GH3023R,GH3024R,GH3025R'

    # 后保支架L
    select_points_dict['c53fb_Houbaozhijia_L_p_10'] = 'KH3026L,KH3027L,KH3028L,KH3029L,KH3030L,KH3031L,KH3032L'

    # 后保支架R
    select_points_dict['c53fb_Houbaozhijia_R_p_10'] = 'KH3026R,KH3027R,KH3028R,KH3029R,KH3030R,KH3031R,KH3032R'

    # 尾灯盒L
    select_points_dict[
        'c53fb_Weidenghe_L_p_10'] = 'KH3033L,KH3034L,KH3035L,KH3036L,KH3037L,KH3038L,KH3039L,KH3040L,KH3041L,KH3042L,' \
                                    'KH3043L '

    # 尾灯盒R
    select_points_dict[
        'c53fb_Weidenghe_R_p_10'] = 'KH3033R,KH3034R,KH3035R,KH3036R,KH3037R,KH3038R,KH3039R,KH3040R,KH3041R,KH3042R,' \
                                    'KH3043R '

    # 后防撞梁安装
    select_points_dict[
        'c53fb_Houfangzhuangliang_p_10'] = 'EH3044L,EH3044R,GP3045L,GP3045R,GP3046L,GP3046R.GP3047L,GP3047R'

    # 后减震器L
    select_points_dict['c53fb_Houjianzhenqi_L_p_11'] = 'KN3048L,KN3049L,KN3050L'

    # 后减震器R
    select_points_dict['c53fb_Houjianzhenqi_R_p_11'] = 'KN3048R,KN3049R,KN3050R'

    # 慢充座
    select_points_dict['c53fb_Manchongzuo_p_11'] = 'GH3051R,GH3052R,GH3053R,GH3054R,GH3055R,GN3056R,GN3057R'

    # A柱 内板L
    select_points_dict[
        'c53fb_Azhuneiban_p_12'] = 'GH3058L,GH3059L,GH3060L,GN3061L,GN3062L,GN3063,KH3064L,GH3065L,GH3066L'

    # A柱 内板R
    select_points_dict[
        'c53fb_Azhuneiban_p_12'] = 'GH3058R,GH3059R,GH3060R,GN3061R,GN3062R,GN3063,KH3064R,GH3065R,GH3066R'

    # B柱内板L
    select_points_dict[
        'c53fb_Bzhuneiban_p_12'] = 'GH3067L,GH3068L,GH3069L,GH3070L,GH3071L,GH3072L,GH3073L,GH3074L,GH3075L'

    # B柱内板R
    select_points_dict[
        'c53fb_Bzhuneiban_p_12'] = 'GH3067R,GH3068R,GH3069R,GH3070R,GH3071R,GH3072R,GH3073R,GH3074R,GH3075R'

    # C 柱内板L
    select_points_dict['c53fb_Czhuneiban_p_12'] = 'GH3076L,GH3077L,GH3078L,GH3079L,GH3080L,GH3081L,GH3082L'

    # C 柱内板R
    select_points_dict['c53fb_Czhuneiban_p_12'] = 'GH3076R,GH3077R,GH3078R,GH3079R,GH3080R,GH3081R,GH3082R'

    # 后隔板
    select_points_dict['c53fb_Hougeban_p_13'] = 'EH3083L,EH3084R,GH3085L,GH3085R,CH3086C,GH3087L,GH3087R'

    # 行李箱铰链
    select_points_dict['c53fb_Xinglixiangjiaolian_p_13'] = 'KH3088L,KH3088R,KH3089L,KH3089R,KH3090L,KH3090R'

    # 后排座椅及衣帽架
    select_points_dict[
        'c53fb_HouzuoyiYimaojia_p_13'] = 'GH3092L,GH3092R,GH3093L,GH3093R,GH3094L,GH3095L,GH3096R,GN3097L,GN3097R,' \
                                         'KH3098L,KH3099L,KH3099R '

    # 顶棚前横梁
    select_points_dict[
        'c53fb_DingpengQianhengliang_p_22'] = 'EH4001L,EH4002R,GH4003L,GH4003R,GH4004L,GH4005R,GH4052L,GH4053R'

    # 顶棚后横梁
    select_points_dict['c53fb_DingpengHouhengliang_p_22'] = 'EH4006L,EH4007R,GH4008R,GH4009C,GH4008L'

    # 天窗
    select_points_dict[
        'c53fb_Tianchuang_p_22'] = 'KH4010R,KH4011R,KH4012L,KH4012R,KN4013C,KN4014L,KN4014R,KN4015L,KN4015R,KN4016L,' \
                                   'KN4016R,KN4017L,KN4017R,KN4018L,KN4018R,KN4019L,KN4019R,KN4020L,KN4020R '



    return select_points_dict



if __name__ == '__main__':
    pass

    # doctest 调用
    # _test()

    data_source = None

    select_points_dict_value = select_points_dict()

    window_1 = tk.Tk()
    window_1.title('三坐标数据可视化分析器v2_20200318')
    pad_x_default = 5
    pad_y_default = 5

    # 第一行布局，数据查找按钮和显示框
    var_file_name = tk.StringVar()

    label_1_1 = tk.Label(window_1, textvariable=var_file_name, width=60, height=2, bg='yellow')
    label_1_1.grid(row=10, column=11, columnspan=20, sticky='w', padx=pad_x_default, pady=pad_y_default, )

    # 读取源数据耗时12秒左右，只在第一次打开时读取，避免每次分析时读取耗时
    def display_read_file():
        var_file_name.set(find_file())
        global data_source
        if data_source is None:
            data_source = read_data()


    button_1 = tk.Button(window_1, text='源数据(.xlsx文件)', width=20, height=1, font=None, command=display_read_file)
    button_1.grid(row=10, column=10, sticky='e', padx=pad_x_default, pady=pad_y_default)

    # 第二行布局，选择比较数据对
    data_list = ['名义值', 'last1', 'last2', 'last3', 'last4', 'last5',
                 'last6', 'last7', 'last8', 'last9', 'last10']

    label_2_1 = tk.Label(window_1, text='参考数据 VS 对比数据')
    label_2_1.grid(row=20, column=10, sticky='e', padx=pad_x_default, pady=pad_y_default)

    compare_choice_first = tk.StringVar()
    compare_choice_first.set('名义值')
    data_compare_option_menu = tk.OptionMenu(window_1, compare_choice_first, *data_list)
    data_compare_option_menu.grid(row=20, column=11, sticky='w', padx=pad_x_default, pady=pad_y_default)

    compare_choice_second = tk.StringVar()
    compare_choice_second.set('last1')
    data_compare_option_menu = tk.OptionMenu(window_1, compare_choice_second, *data_list)
    data_compare_option_menu.grid(row=20, column=12, sticky='w', padx=pad_x_default, pady=pad_y_default)

    # 第三行布局，选择比较平面
    label_3_1 = tk.Label(window_1, height=2, text='选择比较平面（不选择时多维度展示）')
    label_3_1.grid(row=30, column=10, sticky='e', padx=pad_x_default, pady=pad_y_default)

    var_plane_choice = tk.IntVar()
    var_plane_choice.set(0)
    tk.Radiobutton(window_1, text='X-Y平面', variable=var_plane_choice,
                   value=1).grid(row=30, column=11, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='Y-Z平面', variable=var_plane_choice,
                   value=2).grid(row=30, column=12, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='X-Z平面', variable=var_plane_choice,
                   value=3).grid(row=30, column=13, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='Y-X平面', variable=var_plane_choice,
                   value=4).grid(row=31, column=11, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='Z-Y平面', variable=var_plane_choice,
                   value=5).grid(row=31, column=12, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='Z-X平面', variable=var_plane_choice,
                   value=6).grid(row=31, column=13, sticky='w', padx=pad_x_default, pady=pad_y_default)
    tk.Radiobutton(window_1, text='多维视图', variable=var_plane_choice,
                   value=0).grid(row=30, rowspan=2, column=14, sticky='w', padx=pad_x_default, pady=pad_y_default)

    # 第4行布局
    color_limit_scale = tk.Scale(window_1, label='异常显示范围界限设定(0-3)', bg='yellow', from_=0, to=3, resolution=0.05,
                                 length=300,
                                 orient='horizontal')
    color_limit_scale.grid(row=40, column=10, columnspan=3, sticky='w', padx=pad_x_default, pady=pad_y_default)

    # 新增4~5行标签
    list_box_label_1 = tk.Label(window_1, text='备选测点列表')
    list_box_label_1.grid(row=45, column=10, padx=pad_x_default, pady=pad_y_default)

    text_box_label_1 = tk.Label(window_1, bg='pink', text='已选择分析测点，可手动输入，逗号分隔，大写')
    text_box_label_1.grid(row=45, column=12, columnspan=3, padx=pad_x_default, pady=pad_y_default)

    # 第5行布局
    # listbox bind函数，把选择值写入text
    def write_to_text(event):
        listbox_select_value = select_points_c53f_listbox_1.get(select_points_c53f_listbox_1.curselection())
        var_select_point_text.insert('end', select_points_dict_value[listbox_select_value] + '\n')


    var_select_points_c53f_list_values = tk.StringVar()
    var_select_points_c53f_list_values.set(tuple(select_points_dict_value.keys()))
    select_points_c53f_listbox_1 = tk.Listbox(window_1, width=40, height=14,
                                              listvariable=var_select_points_c53f_list_values)
    select_points_c53f_listbox_1.grid(row=50, column=10, padx=pad_x_default, pady=pad_y_default)
    l_y_bar = tk.Scrollbar()
    l_y_bar['command'] = select_points_c53f_listbox_1.yview
    select_points_c53f_listbox_1.configure(yscrollcommand=l_y_bar.set)
    l_y_bar.grid(row=50, column=11, sticky=tk.N + tk.S + tk.E + tk.W)

    # 双击listbox 写入text文本框
    select_points_c53f_listbox_1.bind('<Double-Button-1>', write_to_text)

    var_select_point_text = tk.Text(window_1, width=40, height=20)
    var_select_point_text.grid(row=50, column=12, columnspan=3, sticky='w', padx=pad_x_default,pady=pad_y_default)

    # 开始分析按钮
    start_button = tk.Button(window_1, text='展示分析图', bg='green', command=lambda: chart_display(
        column_m_name=compare_choice_first.get(),
        column_n_name=compare_choice_second.get(),
        plane_choice=var_plane_choice.get(),
        data_source=data_source,
        choose_points=var_select_point_text.get('0.0', 'end'),
        color_limit_num=color_limit_scale.get()
    ))
    start_button.grid(row=60, column=10, columnspan=5, sticky=tk.W+tk.E, padx=pad_x_default, pady=pad_y_default)

    # 显示运行状态信息
    state_text_box_label_1 = tk.Label(window_1, text='程序运行状态栏')
    state_text_box_label_1.grid(row=20, column=16, padx=pad_x_default, pady=pad_y_default)

    run_state_text = tk.Text(window_1, width=40, bg='gray')
    run_state_text.grid(row=30, rowspan=70, sticky=tk.N+tk.S, column=16)

    run_state_text.insert('end', '{}---欢迎使用三坐标数据分析器\n'.format(datetime.now()))
    window_1.mainloop()
