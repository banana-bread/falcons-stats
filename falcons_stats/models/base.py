from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    """Base class for all models."""
    pass

# Create a single SQLAlchemy instance to be used throughout the application
db = SQLAlchemy(model_class=Base)