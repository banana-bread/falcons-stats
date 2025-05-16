from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright
from .exceptions import ScraperHttpError, ScraperParsingError
from falcons_stats.logger import logger
from falcons_stats.models import Base

class BaseScraper(ABC):
    def __init__(self):
        self.parsed_records = []

    @abstractmethod
    def path(self) -> str:
        pass

    @abstractmethod
    def metric_column(self) -> str:
        pass

    @abstractmethod
    def model(self) -> Base:
        pass

    def url(self) -> str:
        return f"https://ocslonline.ca{self.path()}"

    def run(self):
        from urllib.parse import urlparse
        from falcons_stats.services import StatsService

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            domain = urlparse(self.url()).netloc

            for division in StatsService.get_all_divisions():
                page = context.new_page()
                context.clear_cookies()
                context.add_cookies([
                    {"name": "e2elc_gamesdivisionid","value": str(division['id']),"domain": domain,"path": "/",},
                    {"name": "e2elc_top10only","value": "false","domain": domain,"path": "/",}
                ])
                try:
                    logger.info(f"Scraping division {division['name']}")
                    page.goto(self.url(), timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_load_state("networkidle")
                    raw_data = page.content()
                except Exception as e:
                    logger.error(f"Error scraping division {division['name']}", extra={
                        "division_id": division['id'],
                        "url": self.url(),
                        "error": str(e)
                    })
                    raise ScraperHttpError(original_error=e, division_id=division['id'], url=self.url())
                finally:
                    page.close()

                try:
                    logger.info(f"Parsing HTML for division {division['name']}")
                    parsed_data = self.parse_html_response(raw_data, division['teams'])
                except Exception as e:
                    logger.error(f"Error parsing HTML for division {division['name']}", extra={
                        "division_id": division['id'],
                        "url": self.url(),
                        "error": str(e)
                    })
                    raise ScraperParsingError(original_error=e, division_id=division['id'], url=self.url())
                
                self.parsed_records.extend(parsed_data)
                
            browser.close()
        self.refresh_stats()

    
    def parse_html_response(self, raw_data: str, teams: list):
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(raw_data, "html.parser")
        table = soup.find("table", class_="e2e-table")
        rows = table.find_all("tr")[1:]

        team_lookup = {team["name"]: team["id"] for team in teams}
        results = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            team_name = cols[3].text.strip()
            team_id = team_lookup.get(team_name)

            if team_id is None:
                continue 

            results.append({
                "player_name": cols[1].text.strip(),
                "team_id": team_id,
                "metric": int(cols[4].text.strip())
            })
        
        return results
    
    # def refresh_stats(self):
    #     import ipdb; ipdb.set_trace()
    #     pass

    def refresh_stats(self):
        from falcons_stats.models.base import db

        Model = self.model()
        metric_column = self.metric_column()

        # Wipe table
        logger.info(f"Deleting all records from table {Model.__tablename__}")
        db.session.query(Model).delete()

        # Insert fresh data
        logger.info(f"Inserting {len(self.parsed_records)} fresh records into table {Model.__tablename__}")
        instances = [
            Model(
                name=record["player_name"],
                team_id=record["team_id"],
                **{metric_column: record["metric"]}
            )
            for record in self.parsed_records
        ]

        db.session.add_all(instances)
        db.session.commit()
