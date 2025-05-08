import click
from flask import current_app
from .models.base import db
from flask.cli import with_appcontext
from sqlalchemy import text

def init_app(app):
    """Register database functions with the Flask app"""
    # Initialize the app with the extension
    db.init_app(app)

    # Register CLI commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_dev_command)
    app.cli.add_command(seed_db_prod_command)

def init_db():
    """Initialize the database by creating all tables"""
    with current_app.app_context():
        db.create_all()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('seed-dev-db')
@with_appcontext
def seed_db_dev_command():
    """Seed the database with development data including fake players and keepers."""
    seed_db_dev()
    click.echo('Seeded the database with development data.')

@click.command('seed-prod-db')
@with_appcontext
def seed_db_prod_command():
    """Seed the database with production data (divisions and teams only)."""
    seed_db_prod()
    click.echo('Seeded the database with production data.')

def seed_db_dev():
    """Seed the database with development data including fake players and keepers."""
    # Clear existing data
    db.session.execute(text("DELETE FROM keepers"))
    db.session.execute(text("DELETE FROM players"))
    db.session.execute(text("DELETE FROM teams"))
    db.session.execute(text("DELETE FROM divisions"))

    # Import seed data
    from .seeds import get_divisions, get_teams, generate_random_players, generate_random_keepers

    # Create divisions and teams
    divisions = get_divisions()
    teams = get_teams()

    # Add divisions and teams to the session
    db.session.add_all(divisions)
    db.session.add_all(teams)

    # Commit to get IDs for teams
    db.session.commit()

    # Create players and keepers
    players = generate_random_players(teams)
    keepers = generate_random_keepers(teams)

    # Add players and keepers to the session
    db.session.add_all(players)
    db.session.add_all(keepers)

    # Commit all changes
    db.session.commit()

def seed_db_prod():
    """Seed the database with production data (divisions and teams only)."""
    # Clear existing data for teams and divisions
    db.session.execute(text("DELETE FROM teams"))
    db.session.execute(text("DELETE FROM divisions"))

    # Import seed data
    from .seeds import get_divisions, get_teams

    # Create divisions and teams
    divisions = get_divisions()
    teams = get_teams()

    # Add divisions and teams to the session
    db.session.add_all(divisions)
    db.session.add_all(teams)

    # Commit all changes
    db.session.commit()

