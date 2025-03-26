import time
from schedule import every, repeat, run_pending
from falcons_stats.scrapers import GoalScorersScraper, CleanSheetsScraper, ScraperHttpError
from falcons_stats.logger import logger


@repeat(every().day.at("02:00", "America/Toronto"))
def run_scrapers():
    scrapers = [
        GoalScorersScraper(),
        CleanSheetsScraper()
    ]

    for scraper in scrapers:
        try:
            scraper.run()
        except ScraperHttpError as e:
            logger.error(f"Scraper {scraper.__class__.__name__} failed", extra={
                "division_id": e.division_id,
                "url": e.url,
                "error": str(e.original_error)
            })
            # Continue with the next scraper
            continue
        except Exception as e:
            logger.error(f"Unexpected error in scraper {scraper.__class__.__name__}", extra={
                "error": str(e)
            })
            # Continue with the next scraper
            continue

while True:
    run_pending()
    time.sleep(1)