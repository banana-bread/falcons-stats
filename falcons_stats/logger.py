from flask import Flask
import sys, logging, time, socket, os
from datetime import datetime, timezone
from pythonjsonlogger import json

logger = logging.getLogger(__name__)

class DailyRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        self.current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.base_filename = filename
        self.current_filename = self._get_filename()
        super().__init__(self.current_filename, mode, encoding, delay)

    def _get_filename(self):
        return self.base_filename.replace('{date}', self.current_date)

    def emit(self, record):
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        if current_date != self.current_date:
            self.current_date = current_date
            self.close()
            self.baseFilename = self._get_filename()
            self._open()
        super().emit(record)

def init_log_handler(app: Flask):
    environment = app.config.get('ENVIRONMENT', 'production')
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
    
    # Create log file handlers with date placeholder
    app_log_file = os.path.join(log_dir, f"{app.name}-{{date}}.log")
    
    # Application log handler
    file_handler = DailyRotatingFileHandler(app_log_file)
    file_handler.setFormatter(fmt)
    app.logger.addHandler(file_handler)
    
    # Werkzeug (web server) log handler
    werkzeug_log_file = os.path.join(log_dir, f"werkzeug-{{date}}.log")
    werkzeug_handler = DailyRotatingFileHandler(werkzeug_log_file)
    werkzeug_handler.setFormatter(fmt)
    logging.getLogger("werkzeug").addHandler(werkzeug_handler)
    
    # Log the startup
    app.logger.info(f"Application logging to {file_handler.current_filename}")
