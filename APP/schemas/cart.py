from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

class CartItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(default=1, ge=1)


# ==========================================
# CART ITEM RESPONSE
# ==========================================

class CartItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)