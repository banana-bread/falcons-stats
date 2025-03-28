from typing import List
from falcons_stats.models.base import db
from falcons_stats.utils import sanitize_team_name

class StatsService:
    @staticmethod
    def get_top_scorers(limit: int = 10) -> List[dict]:
        from falcons_stats.queries import get_top_scorers
        results = db.session.execute(get_top_scorers(limit)).all()
        return [
            {
                'player_name': player.name,
                'team_name': sanitize_team_name(team_name),
                'goals': player.goals
            }
            for player, team_name in results
        ]
    
    @staticmethod
    def get_top_keepers(limit: int = 10) -> List[dict]:
        from falcons_stats.queries import get_top_keepers
        results = db.session.execute(get_top_keepers(limit)).all()
        return [
            {
                'keeper_name': keeper.name,
                'team_name': sanitize_team_name(team_name),
                'clean_sheets': keeper.clean_sheets
            }
            for keeper, team_name in results
        ]
