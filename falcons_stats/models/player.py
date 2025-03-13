from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Player(Base):
    __tablename__ = "players"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))
    name: Mapped[str] = mapped_column(String(100))
    goals: Mapped[int] = mapped_column(default=0)
    
    # Relationships
    division: Mapped["Division"] = relationship(back_populates="players") # type: ignore
    
    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, name={self.name!r}, goals={self.goals!r})"