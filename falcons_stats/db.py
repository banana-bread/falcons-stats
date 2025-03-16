import click
from flask import current_app
from .models.base import db
from .models import Player, Keeper, Team, Division
from flask.cli import with_appcontext
from sqlalchemy import text
import random

def init_app(app):
    """Register database functions with the Flask app"""
    # Initialize the app with the extension
    db.init_app(app)
    
    # Register CLI command
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_dev_command)

def init_db():
    """Initialize the databse by creating all tables"""
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
    """Seed the database with fresh initial data"""
    seed_db_dev()
    click.echo('Seeded the database.')

######### SEEDING STUFF BELOW (SHOULD PROBABLY MOVE TO NEW FILE) #########
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", 
                  "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", 
                  "Susan", "Jessica", "Sarah", "Karen", "Lisa"]
    
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
                  "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris",
                  "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

def seed_db_dev():
    """Seed the database with fresh initial data"""
    # Clear existing data
    db.session.execute(text("DELETE FROM keepers"))
    db.session.execute(text("DELETE FROM players"))
    db.session.execute(text("DELETE FROM teams"))
    db.session.execute(text("DELETE FROM divisions"))
    
    # Create divisions and team first
    divisions = make_divisions()
    teams = make_teams()

    db.session.add_all(divisions)
    db.session.add_all(teams)

    # Commit divisions and teams to get ids
    db.session.commit()

    # Create players and keepers with team ids
    players = make_players(teams)
    keepers = make_keepers(teams)

    db.session.add_all(players)
    db.session.add_all(keepers)    

    # Commit players and keepers
    db.session.commit()


def seed_db_prod():
    """Seed the database with some initial data"""
    pass

def make_divisions() -> list[Division]:
    """ Seed the database with real divisions and their OCSL ids """
    return [
        Division(id=1, name='MP'),
        Division(id=66, name='MC1'),
        Division(id=67, name='MC2'),
        Division(id=92, name='MR2'),
        Division(id=74, name='MR3'),
        Division(id=75, name='MR4'),
        Division(id=80, name='MOT1'),
        Division(id=58, name='MOT2'),
        Division(id=15, name='MOT3'),
        Division(id=87, name='MOT4'),
        Division(id=69, name='WC2'),
        Division(id=27, name='WR1'),
        Division(id=29, name='WR2'),
    ]

def make_teams() -> list[Team]:
    # TODO: not real team ids, just for testing
    return [
        Team(name='Ottawa Falcons MP', division_id=1),
        Team(name='Ottawa Falcons MC1', division_id=66),
        Team(name='Ottawa Falcons MC2', division_id=67),
        Team(name='Ottawa Falcons MR2', division_id=92),
    ]

def make_players(teams: list[Team]) -> list[Player]:
    return [
        Player(
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            team_id=team.id,
            goals=random.randint(1, 10)
        )
        for team in teams
        for _ in range(random.randint(3, 5))
    ]

def make_keepers(teams: list[Team]) -> list[Keeper]:
    return [
        Keeper(
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            team_id=team.id,
            clean_sheets=random.randint(1, 3)
        )
        for team in teams
    ]

