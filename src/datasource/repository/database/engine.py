from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class DatabaseEngine:
    def __init__(self):
        DATABASE_URL = "postgresql+psycopg2://postgres:example@localhost:5432/postgres"
        self.engine = create_engine(
            DATABASE_URL, 
            echo=True,
            pool_pre_ping=True)

def session_factory(db_engine: DatabaseEngine) -> Session:
    return db_engine.get_session()