from .base_scraper import BaseScraper
from falcons_stats.models import Keeper

class CleanSheetsScraper(BaseScraper):
    def path(self) -> str:
        return "/shutouts"

    def metric_column(self) -> str:
        return "clean_sheets"
    
    def model(self) -> Keeper:
        return Keeper