import time
import click
from flask.cli import with_appcontext
from schedule import every, repeat, run_pending
from falcons_stats.logger import logger


@repeat(every().day.at("06:00")) # UTC time
def run_scrapers():
    logger.info("Running scrapers... but not really because this is a dummy function until we implement the real thing")
    return

    from falcons_stats.services import ScraperService
    results = ScraperService.run_scrapers()
    logger.info(f"Scraping completed. Success: {len(results['success'])}, Failed: {len(results['failed'])}")

@click.command('run-scheduler')
@with_appcontext
def run_scheduler_command():
    logger.info("Starting scheduler")

    while True:
        run_pending()
        time.sleep(1)  

def register_commands(app):
    app.cli.add_command(run_scheduler_command)
