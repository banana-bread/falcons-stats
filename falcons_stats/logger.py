from flask import Flask
import sys, logging, time, watchtower
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)

def init_log_handler(app: Flask):
    environment = app.config.get('ENVIRONMENT', 'production')
    log_level = logging.DEBUG if environment == 'development' else logging.INFO

    # Configure root logger to use JSON format for console output
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add stdout handler with JSON formatting
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = jsonlogger.JsonFormatter(
        "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    stdout.setFormatter(fmt)
    root_logger.addHandler(stdout)

    # Set formatter to use UTC time
    for handler in root_logger.handlers:
        handler.formatter.converter = time.gmtime
    
    # Add a CloudWatch handler if in production
    if environment == 'production':
        handler = watchtower.CloudWatchLogHandler(log_group_name=app.name)
        handler.setFormatter(fmt)
        app.logger.addHandler(handler)
        logging.getLogger("werkzeug").addHandler(handler)
