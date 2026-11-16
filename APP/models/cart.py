
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from APP.database.connection import Base


class Cart(Base):

    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_cart"),
    )

    # Cart belongs to one user
    user = relationship(
        "User",
        back_populates="cart"
    )

    # Cart contains multiple items
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


