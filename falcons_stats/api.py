from flask import Blueprint
import re

api = Blueprint('api', __name__)

@api.route('/leading-scorers')
def leading_scorers():
    goal_scorers = [
        { 'player_name': 'Jennifer FURMAN', 'team_name': 'Ottawa Falcons WR2', 'division_id': 29, 'goals': 19 },
        { 'player_name': 'Travis FENNING', 'team_name': 'Ottawa Falcons Azzurri MR2', 'division_id': 92, 'goals': 15 },
        { 'player_name': 'Adriano DRAMISINO', 'team_name': 'Falcons Red MC2', 'division_id': 67, 'goals': 10 },
        { 'player_name': 'Ryan MORRISON', 'team_name': 'Falcons Red MC2', 'division_id': 67, 'goals': 5 },
    ]
    goal_scorers = _strip_team_name(goal_scorers)
    return {
        'goal_scorers': goal_scorers
    }

@api.route('/clean-sheets')
def clean_sheets():
    clean_sheets = [
        { "player_name": "Ryan MORRISON", "team_name": "Falcons Red MC2", "division_id": 67, "clean_sheets": 10 },
        { "player_name": "Trevor MOBBS", "team_name": "Falcons Red MC2", "division_id": 29, "clean_sheets": 5 },
        { "player_name": "Adriano DRAMISINO", "team_name": "Falcons Red MC2", "division_id": 67, "clean_sheets": 0 },
    ]
    clean_sheets = _strip_team_name(clean_sheets)
    return {
        'clean_sheets': clean_sheets
    }

def _strip_team_name(players):
    for player in players:
        player['team_name'] = re.sub(r'\b(ottawa falcons|falcons)\b', '', player['team_name'], flags=re.IGNORECASE).strip()
        del player['division_id']
    return players