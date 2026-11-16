from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from APP.database.connection import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    quantity = Column(Integer, nullable=False)

    # Product can appear in multiple carts
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    # Product can appear in multiple orders
    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )