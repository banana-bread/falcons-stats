from flask import Blueprint
from falcons_stats.services import StatsService
from falcons_stats.logger import logger

api = Blueprint('api', __name__)

@api.route('/leading-scorers')
def leading_scorers():
    logger.info('Getting leading scorers')
    return {'scorers': StatsService.get_top_scorers()}

@api.route('/leading-keepers')
def clean_sheets():
    # TODO: should remove, only for testing
    logger.info('Getting leading keepers')
    return {'keepers': StatsService.get_top_keepers()}
