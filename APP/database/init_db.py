from APP.database.connection import Base, engine

# Register all models
from APP.models.product import Product
from APP.models.user import User
from APP.models.cart import Cart
from APP.models.CartItem import CartItem
from APP.models.order import Order
from APP.models.OrderItem import OrderItem


# Create database tables
Base.metadata.create_all(bind=engine)

print("All database tables created successfully!")


from sqlalchemy import inspect

inspector = inspect(engine)

tables = inspector.get_table_names()

print("Database Tables:")

for table in tables:
    print(table)