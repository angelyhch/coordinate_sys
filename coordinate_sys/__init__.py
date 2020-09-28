from flask import Flask
from .settings import config
import os
from .logger_class import logger
from .blueprints.index import hello_bp
from .extensions import db, bootstrap, toolbar


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        from sqlalchemy import create_engine, inspect
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db_inspector = inspect(engine)
        return dict(db=db, app=app, db_inspector=db_inspector)


def register_blueprints(app):
    app.register_blueprint(hello_bp, url_prefix='/hello')


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # 初始化app程序
    app = Flask('coordinate_sys')
    app.config.from_object(config[config_name])
    db.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)

    # 注册app信息
    register_shell_context(app)
    register_blueprints(app)

    return app


app = create_app()
root_path = app.root_path



