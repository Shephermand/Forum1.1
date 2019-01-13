from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def createApp():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:han1345@localhost:3306/ajax"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = "zheshijiyezhongwenmiyao"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 关联db与app
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    return app






