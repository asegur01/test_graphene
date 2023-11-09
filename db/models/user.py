from typing import List

from sqlalchemy import String, Integer, Boolean, Float, Column
from sqlalchemy.orm import relationship

from db.models.sql_models import Base
from db.models.address import Address

class User(Base):
    __tablename__ = "user_account"
    id: int = Column(Integer, primary_key=True, autoincrement="auto")
    name: str = Column(String)
    last_name: str = Column(String)
    age: int = Column(Integer)
    is_alive: bool = Column(Boolean)
    height: float = Column(Float)
    weigth: int = Column(Integer)
    fullname: str = Column(String)
    
    addresses: List[Address] = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"