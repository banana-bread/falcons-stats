from flask import Blueprint
from falcons_stats.services import StatsService

api = Blueprint('api', __name__)

@api.route('/leading-scorers')
def leading_scorers():
    return {'scorers': StatsService.get_top_scorers()}

@api.route('/leading-keepers')
def clean_sheets():
    return {'keepers': StatsService.get_top_keepers()}

@api.route('/club-stats')
def club_stats():
    return {'club_stats': StatsService.get_club_stats()}
