from flask import Blueprint
import re

api = Blueprint('api', __name__)

@api.route('/leading-scorers')
def leading_scorers():
    return {
        'goal_scorers': _mock_db_call_for_top_scorers()
    }

def _mock_db_call_for_top_scorers():
    goal_scorers = [
        { 'player_name': 'Jennifer FURMAN', 'team_name': 'Ottawa Falcons WR2', 'division_id': 29, 'goals': 19 },
        { 'player_name': 'Travis FENNING', 'team_name': 'Ottawa Falcons Azzurri MR2', 'division_id': 92, 'goals': 15 },
        { 'player_name': 'Adriano DRAMISINO', 'team_name': 'Falcons Red MC2', 'division_id': 67, 'goals': 10 },
        { 'player_name': 'Ryan MORRISON', 'team_name': 'Falcons Red MC2', 'division_id': 67, 'goals': 5 },
    ]

    # TODO: will probably filter this stuff out before saving to db
    for scorer in goal_scorers:
        scorer['team_name'] = re.sub(r'\b(ottawa falcons|falcons)\b', '', scorer['team_name'], flags=re.IGNORECASE).strip()
        del scorer['division_id']

    return goal_scorers

