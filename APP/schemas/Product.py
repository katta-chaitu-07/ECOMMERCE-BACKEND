
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# ----------------------------------------
# Product Creation Schema
# ----------------------------------------

class ProductCreate(BaseModel):

    id: int = Field(gt=0)

    name: str = Field(min_length=2, max_length=100)

    price: float = Field(gt=0)

    quantity: int = Field(ge=0)

    image_url: Optional[str] = None


# ----------------------------------------
# Product Response Schema
# ----------------------------------------

class ProductResponse(BaseModel):

    id: int

    name: str

    price: float

    quantity: int

    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------
# Product Update Schema
# ----------------------------------------

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    price: Optional[float] = Field(default=None, gt=0)

    quantity: Optional[int] = Field(default=None, ge=0)

    image_url: Optional[str] = None
