# tests/test_api.py
import pytest

def test_get_leading_scorers(client, sample_players):
    response = client.get('/leading-scorers')
    assert response.status_code == 200, "Expected 200 OK from /leading-scorers endpoint"

    scorers = response.json['scorers']

    assert isinstance(scorers, list), "Expected 'scorers' to be a list in the response"

    assert all(
        'player_name' in s and 'team_name' in s and 'goals' in s for s in scorers
    ), "Each scorer must have 'player_name' and 'goals' keys"

    goals = [s['goals'] for s in scorers]
    assert goals == sorted(goals, reverse=True), "Scorers are not sorted by goals descending"


def test_get_leading_keepers(client, sample_keepers):
    response = client.get('/leading-keepers')
    assert response.status_code == 200, "Expected 200 OK from /leading-keepers endpoint"

    keepers = response.json['keepers']

    assert isinstance(keepers, list), "Expected 'keepers' to be a list in the response"

    assert all(
        'keeper_name' in k and 'team_name' in k and 'clean_sheets' in k for k in keepers
    ), "Each keeper must have 'keeper_name' and 'clean_sheets' keys"

    clean_sheets = [k['clean_sheets'] for k in keepers]
    assert clean_sheets == sorted(clean_sheets, reverse=True), "Keepers are not sorted by clean sheets descending"

def test_error_handling(client):
    response = client.get('/non-existent-endpoint')
    assert response.status_code == 404, "Was expecting 404 Not Found"