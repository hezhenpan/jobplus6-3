from flask import Flask, render_template
from jobplus.config import configs
from jobplus.models import db
from flask_migrate import Migrate

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    # 数据库的初始化
    db.init_app(app)
    Migrate(app, db)

    register_blueprints(app)

    return app


# 注册蓝图的函数
def register_blueprints(app):
    from .handlers import front, jobs, company, admin
    app.register_blueprint(front)
    app.register_blueprint(jobs)
    app.register_blueprint(company)
    app.register_blueprint(admin)

