from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Division(Base):
    __tablename__ = "divisions"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True) # Mapped to OCSL division id
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relationships
    teams: Mapped[List["Team"]] = relationship( # type: ignore
        back_populates="division", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"Division(id={self.id!r}, name={self.name!r})"
    
    @property
    def serialize(self) -> dict:
        return { 'id': self.id, 'name': self.name }