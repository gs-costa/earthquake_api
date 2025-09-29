from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import Environment

engine = create_engine(
    url=Environment.POSTGRES_DATABASE_URI,
    pool_size=500,
    max_overflow=25,
    pool_timeout=60,
    pool_recycle=600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
