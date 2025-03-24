from flask import Flask
import sys, logging, time, watchtower
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)

def init_log_handler(app: Flask):
    environment = app.config.get('ENVIRONMENT', 'production')
    log_level = logging.DEBUG if environment == 'development' else logging.INFO
    
    # Configure app logger instead of root logger
    app.logger.setLevel(log_level)
    
    # Create and add JSON formatter to app logger
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = jsonlogger.JsonFormatter(
        "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    stdout.setFormatter(fmt)
    stdout.formatter.converter = time.gmtime
    
    # Only add handlers if they don't exist already
    if not any(isinstance(h, logging.StreamHandler) for h in app.logger.handlers):
        app.logger.addHandler(stdout)
    
    # Make CloudWatch logging non-blocking in production
    if environment == 'production':
        handler = watchtower.CloudWatchLogHandler(
            log_group_name=app.name,
            stream_name=f"{app.name}-{time.strftime('%Y-%m-%d')}",
            create_log_group=True,
            # Add these lines to make it non-blocking
            send_interval=5,  # seconds
            max_batch_size=10000,
            max_batch_count=100
        )
        app.logger.addHandler(handler)