from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from .models import Player, Keeper, Team

def get_top_scorers(limit:int=10) -> list[dict]:
    return (
        select(Player, Team.name.label('team_name'))
            .join(Team, Player.team_id == Team.id)
            .options(joinedload(Player.team))
            .order_by(desc(Player.goals))
            .limit(limit)
    )

def get_top_keepers(limit:int=10) -> list[dict]:
    return (
        select(Keeper, Team.name.label('team_name'))
            .join(Team, Keeper.team_id == Team.id)
            .options(joinedload(Keeper.team))
            .order_by(desc(Keeper.clean_sheets))
            .limit(limit)
    )
