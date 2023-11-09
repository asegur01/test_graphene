from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("sqlite://", connect_args={'check_same_thread': False}, echo=True)

session = Session(engine)

def get_db():
    try:
        yield session
    finally:
        session.close()