from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from APP.database.connection import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        String(20),
        default="pending",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Order belongs to one user
    user = relationship(
        "User",
        back_populates="orders"
    )

    # Order contains multiple order items
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )