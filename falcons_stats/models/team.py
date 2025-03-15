from typing import List, Union
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Team(Base):
    __tablename__ = "teams"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationships
    division: Mapped["Division"] = relationship(back_populates="teams") # type: ignore
    
    players: Mapped[List["Player"]] = relationship( # type: ignore
        back_populates="team", cascade="all, delete-orphan"
    )
    
    keepers: Mapped[List["Keeper"]] = relationship( # type: ignore
        back_populates="team", cascade="all, delete-orphan"
    )
    
    @property
    def members(self) -> List[Union["Player", "Keeper"]]: # type: ignore
        """Return all team members (players and keepers)"""
        return self.players + self.keepers
    
    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r})"
    
    @property
    def serialize(self) -> dict:
        return {'id': self.id, 'name': self.name }