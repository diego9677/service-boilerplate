from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings

engine = create_engine(settings.DB_URL, future=True)  # echo true for development mode
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


class Model(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=False), default=func.now())
    updated_at = Column(DateTime(timezone=False), default=func.now(), onupdate=func.now())
