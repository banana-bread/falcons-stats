import os

from flask import Flask

# Factory function that gets called by the WSGI server
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints (import routes)
    from .api import api as api_bp
    app.register_blueprint(api_bp)

    # Initialize the database
    from . import db
    db.init_app(app)

    # Initialize models
    from .models import init_models
    init_models(app)

    # Initialize logging
    from .logger import init_log_handler, logger
    init_log_handler(app)

    return app
