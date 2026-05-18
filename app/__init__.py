from flask import Flask

from .config import Config
from .extensions import db, login_manager
from .routes.api import api_bp
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .services.robot_client import RobotClient


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
        RobotClient.reset_instance()

    return app
