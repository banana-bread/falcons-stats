from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Keeper(Base):
    __tablename__ = "keepers"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String(100))
    clean_sheets: Mapped[int] = mapped_column(default=0)
    
    # Relationship
    team: Mapped["Team"] = relationship(back_populates="keepers") # type: ignore
    
    def __repr__(self) -> str:
        return f"Keeper(id={self.id!r}, name={self.name!r}, clean_sheets={self.clean_sheets!r})"
    
    @property
    def serialize(self) -> dict:
        return { 'id': self.id, 'name': self.name, 'clean_sheets': self.clean_sheets }
