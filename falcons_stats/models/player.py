from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Player(Base):
    __tablename__ = "players"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String(100))
    goals: Mapped[int] = mapped_column(default=0)
    
    # Relationships
    team: Mapped["Team"] = relationship(back_populates="players") # type: ignore
    
    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, name={self.name!r}, goals={self.goals!r})"
    
    @property
    def serialize(self) -> dict:
        return { 'id': self.id, 'name': self.name, 'goals': self.goals }