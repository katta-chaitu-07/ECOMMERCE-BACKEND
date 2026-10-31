from sqlalchemy import Column, Integer, Float , String, DateTime, ForeignKey

from APP.database.connection import Base

from sqlalchemy.sql import func


class Cart(Base):


    __tablename__ = "carts"

    id = Column(Integer, primary_key = True, index = True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable = True)

    created_at = Column(DateTime(timezone = True) , server_default = func.now())

