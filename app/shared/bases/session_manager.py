from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_sessionmaker_instance(uri: str) -> scoped_session:
    engine = create_engine(uri, pool_pre_ping=True, encoding="utf-8")
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
