from flask import Flask, request
from coordinate_sys.settings import config
import os
from coordinate_sys.logger_class import logger
from coordinate_sys.blueprints.coordinate import coordinate_bp
from coordinate_sys.blueprints.process import process_bp
from coordinate_sys.extensions import db, bootstrap, toolbar, mail, cache, db_inspector

#todo:待确认shell环境设置

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        from coordinate_sys.emails import send_mail

        return dict(db=db, db_inspector=db_inspector, app=app, send_mail=send_mail)


def register_blueprints(app):
    app.register_blueprint(coordinate_bp)
    app.register_blueprint(process_bp)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # 初始化app程序
    app = Flask('coordinate_sys')
    app.config.from_object(config[config_name])
    db.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # 注册app信息
    register_shell_context(app)
    register_blueprints(app)
    return app


app = create_app()
root_path = app.root_path
app.config['UPLOAD_PATH'] = os.path.join(root_path, 'static\\data_temp')
app.config['TABLE_UPLOAD_PATH'] = os.path.join(root_path, 'static\\process_table_upload_temp')

@app.before_request
def log_ip_url():
    ip = request.remote_addr
    url = request.url

    logger.info(f'\nip：【{ip}】; url：【{url}】')
