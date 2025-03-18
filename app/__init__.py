from flask import Flask
from config import config


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    from app.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from app.dashboard import dashboard as dashboard_blueprint

    app.register_blueprint(dashboard_blueprint)

    return app
