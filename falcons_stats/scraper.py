import requests

# TODO: move to db probably
DIVISION_ID_TO_NAME = {
    67: "Men C2",
    92: "Men R2",
    29: "Women R2",
}

GOAL_SCORERS_URL = "https://ocslonline.ca/goal-scorers/"

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.cookies = {
            "e2elc_gamesdivisionid": None,
            "e2elc_top10only": "false",
        }
        self.division_goal_scorers = {}
    
    def get_goal_scorers(self):
        for div_id in DIVISION_ID_TO_NAME:
            raw_response = self.get_goal_scorers_for_division(div_id)
            self.division_goal_scorers[div_id] = self._parse_goal_scorers(raw_response)
        return self.division_goal_scorers

    def get_goal_scorers_for_division(self, division_id):
        self.cookies["e2elc_gamesdivisionid"] = str(division_id)
        return self._make_get_request(GOAL_SCORERS_URL).text
    
    def _make_get_request(self, url):
        # TODO: add error handling
        return self.session.get(url, cookies=self.cookies)
    
    # TODO: here we'll use beautiful soup to parse raw response
    def _parse_goal_scorers(self, raw_response):
        return self._mock_parsing(raw_response)
    
    def _mock_parsing(self, raw_response):
        return [
            { "player_name": "Travis FENNING", "team_name": "Ottawa Falcons Azzurri MR2", "division_id": 92, "goals": 15 },
            { "player_name": "Adriano DRAMISINO", "team_name": "Falcons Red MC2", "division_id": 67, "goals": 5 },
            { "player_name": "Ryan MORRISON", "team_name": "Falcons Red MC2", "division_id": 67, "goals": 5 },
            { "player_name": "Jennifer FURMAN", "team_name": "Ottawa Falcons WR2", "division_id": 29, "goals": 19 },
        ]