
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from db.models.sql_models import Base
# from db.models.user import User

class Address(Base):
    __tablename__ = "address"
    id: int = Column(Integer, primary_key=True, autoincrement="auto")
    
    email_address: str = Column(String)
    user_id: int = Column(ForeignKey("user_account.id"))
    
    user = relationship("db.models.user.User", back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"