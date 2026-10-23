from APP.database.connection import Base, engine
from APP.models.product import Product
from sqlalchemy import inspect


# Create tables that do not exist yet
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")


# Verify the tables in the database
inspector = inspect(engine)

print("Tables in database:", inspector.get_table_names())