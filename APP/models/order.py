from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func

from APP.database.connection import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())