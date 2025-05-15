from .base_scraper import BaseScraper
from falcons_stats.models import Player

class GoalScorersScraper(BaseScraper):
    def path(self) -> str:
        return "/goal-scorers"

    def metric_column(self) -> str:
        return "goals"
    
    def model(self) -> Player:
        return Player
