from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_caching import Cache
import os
from sqlalchemy import create_engine, inspect
import pandas as pd


toolbar = DebugToolbarExtension()
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
cache = Cache()


root_path = os.path.normcase(os.path.dirname(__file__))

engine = create_engine('mysql+pymysql://coordinate:coordinate_data@127.0.0.1:3306/coordinate_data')
# engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)  #todo: 利用env未成功
db_inspector = inspect(engine)


class Dbobj:
    '''
    数据库连接实例
    engine 是 create_engine返回对象。
    '''
    def __init__(self, engine):
        self.engine = engine

    def excel_to_table(self, read_excel_name, to_table_name, temp_folder=r"static\process_data_temp", to_schema='coordinate_data', header=0, index_col=None):
        # 设定读取数据源地址
        excel_path = os.path.join(root_path, temp_folder, read_excel_name)
        # 读取EXCEL数据
        df1 = pd.read_excel(excel_path, header=header, index_col=index_col)
        # EXCEL数据写入数据库
        df1.to_sql(to_table_name, self.engine, schema=to_schema, if_exists='replace')  # todo: 以后要和三坐标分析拆分数据库或者拆表

    def read_table(self, table_name, index_col='index'):
        df_read = pd.read_sql_table(table_name, self.engine, index_col=index_col)
        return df_read


