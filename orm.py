from typing import List

from sqlalchemy.orm import Session

from model import UserInput
from db.models.user import User
from db.models.address import Address


def insert_user(user: UserInput, db: Session) -> User:
    if user.addresses is None:
        new_user = User(
            name=user.name,
            age=user.age,
            is_alive=user.is_alive,
            last_name=user.last_name,
            height=user.height,
            weigth=user.weigth,
            fullname=user.full_name
        )
    else:
        addresses = [Address(email_address=item.email) for item in user.addresses]

        new_user = User(
            name=user.name,
            age=user.age,
            is_alive=user.is_alive,
            last_name=user.last_name,
            height=user.height,
            weigth=user.weigth,
            fullname=user.full_name,
            addresses=addresses
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user_by_id(db: Session, id: int):
    return db.query(User).where(id=id).one_or_none()
