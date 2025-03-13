from flask import Flask
from .base import Base, db

def init_models(app: Flask):
    """Initialize all models with the Flask application."""
    # Import models here to ensure they're registered with SQLAlchemy
    from .division import Division
    from .player import Player
    from .keeper import Keeper
    
    # This function doesn't need to do anything else - 
    # importing the models is enough to register them with SQLAlchemy
    return