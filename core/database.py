import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import traceback
from config import host, user, password, db_name, port

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
engine = sqlalchemy.create_engine(
    DB_URL, pool_pre_ping=True, future=True, pool_size=20, pool_recycle=3600
)
SessionLocal = orm.sessionmaker(
    autocommit=False, autoflush=True, bind=engine, future=True
)

Base = declarative_base()


def get_db():
    """Get db Session"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        traceback.print_exc()
    finally:
        db.close()
