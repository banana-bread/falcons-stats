from base_scraper import BaseScraper

class GoalScorersScraper(BaseScraper):
    def url(self) -> str:
        return "https://ocslonline.ca/goal-scorers/"

    # TODO: here we'll use beautiful soup to parse raw response
    def parse_html_response(self, raw_data):
        return [
            { "player_name": "Travis FENNING", "team_name": "Ottawa Falcons Azzurri MR2", "division_id": 92, "goals": 15 },
            { "player_name": "Adriano DRAMISINO", "team_name": "Falcons Red MC2", "division_id": 67, "goals": 5 },
            { "player_name": "Ryan MORRISON", "team_name": "Falcons Red MC2", "division_id": 67, "goals": 5 },
            { "player_name": "Jennifer FURMAN", "team_name": "Ottawa Falcons WR2", "division_id": 29, "goals": 19 },
        ]

    def persist_parsed_data(self, parsed_data):
        # TODO: save to db
        pass