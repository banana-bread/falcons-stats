from flask import Flask
from .base import Base, db

all_models = {}

def init_models(app: Flask):
    """Initialize all models with the Flask application."""
    # Import models here to ensure they're registered with SQLAlchemy
    from .division import Division
    from .team import Team
    from .player import Player
    from .keeper import Keeper

     # Store models for shell context
    all_models['db'] = db
    for class_name in Base.__subclasses__():
        all_models[class_name.__name__] = class_name
    
    # Register shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return all_models
    
    # This function doesn't need to do anything else - 
    # importing the models is enough to register them with SQLAlchemy
    return

# Re-export at package level
from .base import Base, db
from .division import Division
from .team import Team 
from .player import Player
from .keeper import Keeper