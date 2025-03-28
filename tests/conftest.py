import pytest
from falcons_stats import create_app
from falcons_stats.models.base import db
from falcons_stats.models import Player, Keeper, Team, Division

@pytest.fixture()
def app():
    """Create and configure a Flask app for testing."""
    # Create app with test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "ENVIRONMENT": "testing"
    }
    
    app = create_app(test_config)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture()
def app_context(app):
    """Create an application context for tests."""
    with app.app_context() as ctx:
        yield ctx

@pytest.fixture()
def db_session(app_context):
    """Provide a database session for testing."""
    return db.session

@pytest.fixture()
def sample_divisions(db_session):
    """Create sample divisions for testing."""
    divisions = [
        Division(id=1, name="Men C2"),
        Division(id=2, name="Men R2"),
        Division(id=3, name="Women R2")
    ]
    db_session.add_all(divisions)
    db_session.commit()
    
    yield divisions
    
    # Clean up is handled by the app fixture

@pytest.fixture()
def sample_teams(db_session, sample_divisions):
    """Create sample teams for testing.
    
    Depends on sample_divisions to ensure the correct division IDs exist.
    """
    # Make sure we have the division IDs from sample_divisions
    division_ids = [div.id for div in sample_divisions]
    
    teams = [
        Team(name="Ottawa Falcons MC2", division_id=sample_divisions[0].id),
        Team(name="Ottawa Falcons MR2", division_id=sample_divisions[1].id),
        Team(name="Ottawa Falcons WR2", division_id=sample_divisions[2].id)
    ]
    db_session.add_all(teams)
    db_session.commit()
    
    yield teams