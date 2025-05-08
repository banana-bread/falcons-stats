"""
Common seed data that is used in both development and production environments.
"""

from falcons_stats.models import Division, Team

def get_divisions() -> list[Division]:
    """Return a list of all divisions with their OCSL IDs."""
    return [
        Division(id=1, name='MP'),
        Division(id=67, name='MC2'),
        Division(id=5, name='MC4'),
        Division(id=92, name='MR2'),
        Division(id=74, name='MR3'),
        Division(id=75, name='MR4'),
        Division(id=58, name='OT1/2'),
        Division(id=15, name='OT3'),
        Division(id=31, name='MOT1'),
        Division(id=49, name='MOT2'),
        Division(id=88, name='MOT4'),
        Division(id=69, name='WC2'),
        Division(id=27, name='WR1'),
        Division(id=29, name='WR2'),
    ]

def get_teams() -> list[Team]:
    """Return a list of all Falcons teams with their division IDs."""
    return [
        Team(name='Ottawa Falcons Red MC2', division_id=67),
        Team(name='Ottawa Falcons Black Cats MOT2', division_id=49),
        Team(name='Ottawa Falcons MR4', division_id=75),
        Team(name='Ottawa Falcons MOT1', division_id=31),
        Team(name='Ottawa Falcons Bohemians MOT4', division_id=88),
        Team(name='Ottawa Falcons Azzurri MR2', division_id=92),
        Team(name='Ottawa Falcons Black MC2', division_id=67),
        Team(name='Ottawa Falcons Boro MR3', division_id=74),
        Team(name='Ottawa Falcons United OT1', division_id=58),
        Team(name='Ottawa Falcons Ramblers MOT4', division_id=88),
        Team(name='Ottawa Falcons OT2', division_id=58),
        Team(name='Ottawa Falcons Hearts WC2', division_id=69),
        Team(name='Ottawa Falcons United WR1', division_id=27),
        Team(name='Ottawa Falcons Strollers OT3', division_id=15),
        Team(name='Ottawa Falcons Fenix OT3', division_id=15),
        Team(name='Ottawa Falcons WR1', division_id=27),
        Team(name='Ottawa Falcons WR2', division_id=29),
        Team(name='Ottawa Falcons MP', division_id=1),
        Team(name='Ottawa Falcons MC4', division_id=5),
        Team(name='Ottawa Falcons MR3', division_id=74),
        Team(name='Ottawa Falcons Bad News Bears MR4', division_id=75),
    ]


