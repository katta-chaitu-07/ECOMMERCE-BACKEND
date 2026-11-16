from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint
)

from sqlalchemy.orm import relationship

from APP.database.connection import Base


class CartItem(Base):

    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="unique_product_per_cart"
        ),

        CheckConstraint(
            "quantity > 0",
            name="check_cart_item_quantity"
        ),
    )

    # CartItem belongs to one cart
    cart = relationship(
        "Cart",
        back_populates="items"
    )

    # CartItem refers to one product
    product = relationship(
        "Product",
        back_populates="cart_items"
    )