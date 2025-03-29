import pytest, random
from falcons_stats import create_app
from falcons_stats.models.base import db
from falcons_stats.models import Player, Keeper, Team, Division

@pytest.fixture()
def app():
    test_config = {
        # "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "ENVIRONMENT": "test"
    }
    
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def app_context(app):
    with app.app_context() as ctx:
        yield ctx

@pytest.fixture()
def db_session(app_context):
    return db.session

@pytest.fixture()
def sample_divisions(db_session):
    divisions = [
        Division(id=i, name =f"MC{i}")
        for i, _ in enumerate(range(random.randint(6, 10)))
    ]
    db_session.add_all(divisions)
    db_session.commit()
    
    yield divisions
    
    # Clean up is handled by the app fixture

@pytest.fixture()
def sample_teams(db_session, sample_divisions):
    teams = []
    for div in sample_divisions:
        for n in range(1, random.randint(1, 4)):
            team = Team(name=f"Ottawa Falcons {div.name}-{n} Team", division_id=div.id)
            teams.append(team)
    
    db_session.add_all(teams)
    db_session.commit()
    
    yield teams

@pytest.fixture()
def sample_players(db_session, sample_teams):
    players = []
    
    for team in sample_teams:
        num_players = random.randint(1, 3)
        
        for _ in range(num_players):
            player = Player(name=generate_random_name(), team_id=team.id, goals=random.randint(0, 15))
            players.append(player)
    
    db_session.add_all(players)
    db_session.commit()
    
    yield players

@pytest.fixture()
def sample_keepers(db_session, sample_teams):
    keepers = [
        Keeper(name=generate_random_name(), team_id=team.id, clean_sheets=random.randint(0, 6))
        for team in sample_teams
    ]
    
    db_session.add_all(keepers)
    db_session.commit()
    
    yield keepers

@pytest.fixture()
def populated_database(sample_divisions, sample_teams, sample_players, sample_keepers):
    """Convenience fixture that depends on all the sample data fixtures, can use
    only this fixture to get a fully populated database
    """
    # No additional setup needed, just combining the dependencies
    pass

def generate_random_name():
    first_names = ["Alex", "Ben", "Charlie", "David", "Emma", "Fiona", 
                  "Grace", "Hannah", "Ian", "Jack", "Kelly", "Liam", 
                  "Michael", "Nathan", "Olivia", "Peter", "Quinn", "Ryan"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", 
                 "Davis", "Garcia", "Wilson", "Martinez", "Anderson", "Taylor", 
                 "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson"]

    return f"{random.choice(first_names)} {random.choice(last_names)}"