"""The database file. Managing the engine and transactions here."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .core.settings import settings

engine = create_engine(settings.DATABASE_URL)  # connects to the database

Base = declarative_base()  # used as a base for all models
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
