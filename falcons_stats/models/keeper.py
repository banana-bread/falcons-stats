from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Keeper(Base):
    __tablename__ = "keepers"
    
    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))
    name: Mapped[str] = mapped_column(String(100))
    clean_sheets: Mapped[int] = mapped_column(default=0)
    
    # Relationship
    division: Mapped["Division"] = relationship(back_populates="keepers") # type: ignore
    
    def __repr__(self) -> str:
        return f"Keeper(id={self.id!r}, name={self.name!r}, clean_sheets={self.clean_sheets!r})"
    
    @property
    def serialize(self) -> dict:
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'division_id': self.division_id,
            'name': self.name,
            'clean_sheets': self.clean_sheets
        }