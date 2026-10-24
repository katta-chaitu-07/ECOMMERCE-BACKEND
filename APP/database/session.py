from sqlalchemy.orm import sessionmaker
from APP.database.connection import engine

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False
)