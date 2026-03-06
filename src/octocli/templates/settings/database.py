from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import SettingsBase

settings = SettingsBase()

SQL_DB_URL = (
    f"mysql+mysqldb://"
    f"{settings.db_user}"
    f":{settings.db_pass}"
    f"@{settings.db_host}"
    f":{settings.db_port}"
    f"/{settings.db_name}"
)

engine = create_engine(
    SQL_DB_URL,
    pool_size=15,
    max_overflow=7,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
