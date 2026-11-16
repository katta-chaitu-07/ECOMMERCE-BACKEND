
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from APP.database.dependencies import get_db
from APP.security.dependencies import get_current_user

from APP.models.cart import Cart
from APP.models.cart_item import CartItem
from APP.models.product import Product
from APP.models.user import User


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# --------------------------------------------------
# Helper: Get existing cart or create a new cart
# --------------------------------------------------

def get_or_create_cart(db: Session, user_id: int):

    cart = db.query(Cart).filter(
        Cart.user_id == user_id
    ).first()

    if cart is None:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


# --------------------------------------------------
# 1. ADD PRODUCT TO CART
# --------------------------------------------------

@router.post("/add/{product_id}", status_code=status.HTTP_200_OK)
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart = get_or_create_cart(db, current_user.id)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    existing_quantity = cart_item.quantity if cart_item else 0
    new_quantity = existing_quantity + quantity

    if new_quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.quantity} units are available"
        )

    try:
        if cart_item:
            cart_item.quantity = new_quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)

        db.commit()
        db.refresh(cart_item)

        return {
            "message": "Product added to cart successfully",
            "product_id": product_id,
            "quantity": cart_item.quantity
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to add product to cart"
        )


# --------------------------------------------------
# 2. VIEW CART
# --------------------------------------------------

@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).options(
        joinedload(Cart.items).joinedload(CartItem.product)
    ).filter(
        Cart.user_id == current_user.id
    ).first()

    if cart is None:
        return {
            "cart_id": None,
            "items": [],
            "total_amount": 0.0,
            "message": "Your cart is empty"
        }

    items = []
    total_amount = 0.0

    for item in cart.items:

        product = item.product

        if product is None:
            continue

        subtotal = float(product.price) * item.quantity
        total_amount += subtotal

        items.append({
            "cart_item_id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "unit_price": float(product.price),
            "quantity": item.quantity,
            "subtotal": round(subtotal, 2)
        })

    return {
        "cart_id": cart.id,
        "items": items,
        "total_amount": round(total_amount, 2)
    }


# --------------------------------------------------
# 3. UPDATE CART ITEM QUANTITY
# --------------------------------------------------

@router.put("/update/{product_id}")
def update_cart_item(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if quantity > product.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.quantity} units are available"
        )

    cart_item.quantity = quantity

    try:
        db.commit()
        db.refresh(cart_item)

        return {
            "message": "Cart quantity updated successfully",
            "product_id": product_id,
            "quantity": cart_item.quantity
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update cart"
        )


# --------------------------------------------------
# 4. REMOVE PRODUCT FROM CART
# --------------------------------------------------

@router.delete("/remove/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if cart is None:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    try:
        db.delete(cart_item)
        db.commit()

        return {
            "message": "Product removed from cart successfully",
            "product_id": product_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to remove product from cart"
        )
