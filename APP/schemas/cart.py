from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

class CartItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(default=1, ge=1)


# ==========================================
# UPDATE CART ITEM
# ==========================================

class CartItemUpdate(BaseModel):

    quantity: int = Field(ge=1)


# ==========================================
# CART ITEM RESPONSE
# ==========================================

class CartItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# INDIVIDUAL PRODUCT IN CART
# ==========================================

class CartProductResponse(BaseModel):

    product_id: int
    product_name: str
    price: float
    quantity: int
    subtotal: float


# ==========================================
# COMPLETE CART RESPONSE
# ==========================================

class CartResponse(BaseModel):

    cart_id: int
    user_id: int
    items: list[CartProductResponse]
    total_price: float