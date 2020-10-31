from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
toolbar = DebugToolbarExtension()

db = SQLAlchemy()

bootstrap = Bootstrap()

mail = Mail()

