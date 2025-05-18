from flask import Flask
import sys, logging, time, socket, os
from datetime import datetime, timezone
from pythonjsonlogger import json

logger = logging.getLogger(__name__)

def init_log_handler(app: Flask):
    environment = app.config.get('ENVIRONMENT', 'production')
    # log_level = logging.DEBUG if environment == 'development' else logging.INFO
    log_level = logging.INFO

    # Configure root logger to use JSON format for console output
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add stdout handler with JSON formatting
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = json.JsonFormatter(
        "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    stdout.setFormatter(fmt)
    root_logger.addHandler(stdout)

    # Set formatter to use UTC time
    for handler in root_logger.handlers:
        handler.formatter.converter = time.gmtime
    
    # Add a file handler for both development and production
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    hostname = socket.gethostname()
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Create log file handlers
    app_log_file = os.path.join(log_dir, f"{app.name}-{timestamp}.log")
    
    # Application log handler
    file_handler = logging.FileHandler(app_log_file)
    file_handler.setFormatter(fmt)
    app.logger.addHandler(file_handler)
    
    # Werkzeug (web server) log handler
    werkzeug_log_file = os.path.join(log_dir, f"werkzeug-{timestamp}.log")
    werkzeug_handler = logging.FileHandler(werkzeug_log_file)
    werkzeug_handler.setFormatter(fmt)
    logging.getLogger("werkzeug").addHandler(werkzeug_handler)
    
    # Log the startup
    app.logger.info(f"Application logging to {app_log_file}")
