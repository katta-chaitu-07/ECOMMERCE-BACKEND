from APP.database.connection import Base
from sqlalchemy import Integer,String,Float
from sqlalchemy.orm import Mapped,mapped_column


class Product(Base):

    __tablename__ = "products"

    id : Mapped[int] = mapped_column(
        Integer, 
        primary_key = True
    )

    name : Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    price : Mapped[float] = mapped_column(
        Float,
        nullable = False
    )

    quantity : Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )