from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

toolbar = DebugToolbarExtension()

db = SQLAlchemy()

bootstrap = Bootstrap()


