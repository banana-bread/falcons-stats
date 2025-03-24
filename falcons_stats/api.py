from flask import Blueprint
from .models.base import db
from .queries import get_top_scorers, get_top_keepers
from .utils import sanitize_team_name
from falcons_stats.logger import logger

api = Blueprint('api', __name__)

@api.route('/leading-scorers')
def leading_scorers():
    # TODO: should remove, only for testing
    logger.info('Getting leading scorers')
    results = db.session.execute(get_top_scorers()).all()
    return {
        'scorers': [
            {
                'player_name': player.name,
                'team_name': sanitize_team_name(team_name),
                'goals': player.goals
            }
            for player, team_name in results
        ]
    }

@api.route('/leading-keepers')
def clean_sheets():
    # TODO: should remove, only for testing
    logger.info('Getting leading keepers')
    results = db.session.execute(get_top_keepers()).all()
    return {
        'keepers': [
            {
                'keeper_name': keeper.name,
                'team_name': sanitize_team_name(team_name),
                'clean_sheets': keeper.clean_sheets
            }
            for keeper, team_name in results
        ]
    }

