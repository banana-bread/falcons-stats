from falcons_stats.logger import logger
from falcons_stats.scrapers import GoalScorersScraper, CleanSheetsScraper, ScraperHttpError

class ScraperService:
    @staticmethod
    def run_scrapers():
        """Run all scrapers and handle errors appropriately"""
        scrapers = [
            GoalScorersScraper(),
            CleanSheetsScraper()
        ]

        results = {"success": [], "failed": []}
        
        for scraper in scrapers:
            try:
                scraper.run()
                results["success"].append(scraper.__class__.__name__)
            except ScraperHttpError as e:
                logger.error(f"Scraper {scraper.__class__.__name__} failed", extra={
                    "division_id": e.division_id,
                    "url": e.url,
                    "error": str(e.original_error)
                })
                results["failed"].append(scraper.__class__.__name__)
                # Continue with the next scraper
                continue
            except Exception as e:
                logger.error(f"Unexpected error in scraper {scraper.__class__.__name__}", extra={
                    "error": str(e)
                })
                results["failed"].append(scraper.__class__.__name__)
                # Continue with the next scraper
                continue
                
        return results