"""The database file. Managing the engine and transactions here."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .core.settings import settings

engine = create_engine(settings.DATABASE_URL, pool_size=10)  # connects to the database

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
