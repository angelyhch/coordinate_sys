from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os
toolbar = DebugToolbarExtension()

db = SQLAlchemy()

bootstrap = Bootstrap()

mail = Mail()

root_path = os.path.normcase(os.path.dirname(__file__))