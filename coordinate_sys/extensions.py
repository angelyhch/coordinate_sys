from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_caching import Cache
import os
from sqlalchemy import create_engine, inspect
from coordinate_sys.settings import DevelopmentConfig

toolbar = DebugToolbarExtension()
db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
cache = Cache()


root_path = os.path.normcase(os.path.dirname(__file__))

engine = create_engine('mysql+pymysql://coordinate:coordinate_data@127.0.0.1:3306/coordinate_data')
# engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)  #todo: 利用env未成功
db_inspector = inspect(engine)