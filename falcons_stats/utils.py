import re

def sanitize_team_name(name: str) -> str:
    return re.sub(r'\b(ottawa falcons|falcons)\b', '', name, flags=re.IGNORECASE).strip()
