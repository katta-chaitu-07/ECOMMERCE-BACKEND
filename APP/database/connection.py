import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Use PostgreSQL when DATABASE_URL is configured.
# Otherwise, use the local SQLite database.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./ecommerce.db"
)

# SQLite requires this additional connection argument.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


class Base(DeclarativeBase):
    pass