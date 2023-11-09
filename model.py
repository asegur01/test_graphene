
from typing import Optional, List

from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr


class QuerySchema(BaseModel):
    query: str = Field()


class AddressInput(BaseModel):
    email: EmailStr = Field()
    user_id: int = Field(ge=1)


class AddressEmbeded(BaseModel):
    email: EmailStr = Field()


class UserInput(BaseModel):
    name: str = Field(max_length=31)
    last_name: str = Field(max_length=50)
    age: int = Field(ge=0)
    is_alive: bool = Field(default=True)
    height: Decimal = Field(decimal_places=2)
    weigth: int = Field()
    full_name: Optional[str] = Field(default=None, max_length=79, min_length=2)
    addresses: Optional[List[AddressEmbeded]] = Field(default=None, min_length=1)
