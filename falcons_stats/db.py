import click
from flask import current_app
from .models.base import db

def init_db():
    """Initialize the databse by creating all tables"""
    with current_app.app_context():
        db.create_all()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app"""
    # Initialize the app with the extension
    db.init_app(app)
    
    # Register CLI command
    app.cli.add_command(init_db_command)