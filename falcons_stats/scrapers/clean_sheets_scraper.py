from .base_scraper import BaseScraper

class CleanSheetsScraper(BaseScraper):
    def url(self) -> str:
        return "https://ocslonline.ca/shutouts/"

    # TODO: here we'll use beautiful soup to parse raw response
    def parse_html_response(self, raw_data):
        return [
            { "player_name": "Ryan MORRISON", "team_name": "Falcons Red MC2", "division_id": 67, "clean_sheets": 10 },
            { "player_name": "Trevor MOBBS", "team_name": "Falcons Red MC2", "division_id": 29, "clean_sheets": 5 },
            { "player_name": "Adriano DRAMISINO", "team_name": "Falcons Red MC2", "division_id": 67, "clean_sheets": 0 },
        ]

    def persist_parsed_data(self, parsed_data):
        # TODO: save to db
        pass