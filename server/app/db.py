"""The database file. Managing the engine and transactions here."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .core.settings import settings


class Base(DeclarativeBase):
    pass

engine = create_engine(settings.DATABASE_URL)  # connects to the database

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()