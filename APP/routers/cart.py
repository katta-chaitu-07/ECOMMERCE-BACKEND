from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from APP.database.dependencies import get_db

from APP.models.cart import Cart
from APP.models.cart_item import CartItem
from APP.models.product import Product

from APP.schemas.cart import CartItemCreate, CartItemResponse

from APP.security.dependencies import get_current_user


router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"]
)


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

@router.post("/add", response_model=CartItemResponse)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # 1. Check whether the product exists
    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # 2. Find the user's cart
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    # 3. Create a cart if it doesn't exist
    if not cart:

        cart = Cart(user_id=current_user.id)

        db.add(cart)
        db.commit()
        db.refresh(cart)

    # 4. Check whether product already exists in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()

    # 5. Calculate the new quantity
    current_quantity = cart_item.quantity if cart_item else 0

    new_quantity = current_quantity + item.quantity

    # 6. Check available stock
    if new_quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    # 7. Update existing cart item
    if cart_item:

        cart_item.quantity = new_quantity

    # 8. Add new cart item
    else:

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(cart_item)

    # 9. Save changes
    db.commit()
    db.refresh(cart_item)

    return cart_item