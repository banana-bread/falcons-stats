"""
Development-only seed data.
This module contains functions for seeding the database with fake data for development.
"""

import random
from falcons_stats.models import Player, Keeper, Team

# Sample names for generating random player and keeper names
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
              "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
              "Susan", "Jessica", "Sarah", "Karen", "Lisa"]

last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
              "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris",
              "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

def generate_random_players(teams: list[Team]) -> list[Player]:
    """Generate random players for development testing."""
    return [
        Player(
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            team_id=team.id,
            goals=random.randint(1, 10)
        )
        for team in teams
        for _ in range(random.randint(3, 5))
    ]

def generate_random_keepers(teams: list[Team]) -> list[Keeper]:
    """Generate random keepers for development testing."""
    return [
        Keeper(
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            team_id=team.id,
            clean_sheets=random.randint(1, 3)
        )
        for team in teams
    ]
