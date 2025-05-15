from .clean_sheets_scraper import CleanSheetsScraper
from .goal_scorers_scraper import GoalScorersScraper

from .exceptions import ScraperHttpError

import click
from flask.cli import with_appcontext
from falcons_stats.logger import logger

# Dictionary mapping scraper names to their classes
SCRAPERS = {
    'goal_scorers': GoalScorersScraper,
    'clean_sheets': CleanSheetsScraper,
}

@click.command('run-scraper')
@click.argument('scraper_name', required=True)
@with_appcontext
def run_scraper_command(scraper_name):
    """Run a specific scraper by name.

    SCRAPER_NAME is the name of the scraper class to run (e.g., GoalScorersScraper).
    """
    if scraper_name not in SCRAPERS:
        available_scrapers = ', '.join(SCRAPERS.keys())
        click.echo(f"Error: Scraper '{scraper_name}' not found. Available scrapers: {available_scrapers}")
        return

    logger.info(f"Running scraper: {scraper_name}")
    try:
        # Create and run the scraper
        scraper_instance = SCRAPERS[scraper_name]()
        scraper_instance.run()

        click.echo(f"Successfully ran {scraper_name}")
    except Exception as e:
        logger.error(f"Error running scraper {scraper_name}", extra={"error": str(e)})
        click.echo(f"Error running {scraper_name}: {str(e)}")

@click.command('list-scrapers')
@with_appcontext
def list_scrapers_command():
    """List all available scrapers."""
    click.echo("Available scrapers:")
    for scraper_name in SCRAPERS.keys():
        click.echo(f"  - {scraper_name}")

def register_commands(app):
    """Register all scraper-related commands with the Flask app."""
    app.cli.add_command(run_scraper_command)
    app.cli.add_command(list_scrapers_command)