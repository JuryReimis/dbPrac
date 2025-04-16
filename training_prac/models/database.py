from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from training_prac.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class BaseModel(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

Session = sessionmaker(bind=engine)
