from abc import ABC, abstractmethod
import requests
from .exceptions import ScraperHttpError
from falcons_stats.queries import get_divisions
from falcons_stats.models.base import db
class BaseScraper(ABC):

    def __init__(self):
        self.session = requests.Session()
        self.cookies = {
            "e2elc_gamesdivisionid": None,
            "e2elc_top10only": "false",
        }

    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def parse_html_response(self, raw_data):
        pass

    @abstractmethod
    def persist_parsed_data(self, parsed_data):
        pass

    def run(self):
        raw_data = self.get_raw_data()
        parsed_data = self.parse_html_response(raw_data)
        self.persist_parsed_data(parsed_data)
    
    # TODO: may make sense to pass div_ids as params to the constructor, will leave for now though
    def divisions(self):
        return db.session.execute(get_divisions()).all()

    def get_raw_data(self):
        result = {}
        for div_id in self.divisions():
            self.cookies["e2elc_gamesdivisionid"] = str(div_id)
            try:
                response = self.session.get(self.url(), cookies=self.cookies)
                response.raise_for_status()
                result[div_id] = response.text
            except requests.exceptions.RequestException as e:
                raise ScraperHttpError(original_error=e, division_id=div_id, url=self.url())
        return result

        
