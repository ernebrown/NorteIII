from flask import Flask
from flask_cors import CORS


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern
    :param settings_override: Override settings
    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    extensions(app)
    CORS(app)

    from cctwin.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in)
    :param app: Flask application instance
    :return: None
    """

    return None
