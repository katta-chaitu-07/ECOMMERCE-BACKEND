from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from APP.database.dependencies import get_db

from APP.models.cart import Cart
from APP.models.cart_item import CartItem
from APP.models.product import Product

from APP.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartResponse,
    CartProductResponse
)

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
    current_user=Depends(get_current_user)
):

    # 1. Check whether product exists

    product = db.query(Product).filter(
        Product.id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # 2. Find user's cart

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    # 3. Find existing cart item

    cart_item = None

    if cart:

        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item.product_id
        ).first()

    # 4. Calculate new quantity

    current_quantity = cart_item.quantity if cart_item else 0

    new_quantity = current_quantity + item.quantity

    # 5. Check available stock

    if new_quantity > product.quantity:

        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    # 6. Create cart if necessary

    if not cart:

        cart = Cart(user_id=current_user.id)

        db.add(cart)
        db.flush()

    # 7. Update existing item or create new item

    if cart_item:

        cart_item.quantity = new_quantity

    else:

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(cart_item)

    # 8. Save changes

    db.commit()
    db.refresh(cart_item)

    return cart_item


# ==========================================
# GET USER CART
# ==========================================

@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # 1. Find user's cart

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:

        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    # 2. Retrieve cart items

    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.id
    ).all()

    items = []

    total_price = 0

    # 3. Process each cart item

    for cart_item in cart_items:

        product = db.query(Product).filter(
            Product.id == cart_item.product_id
        ).first()

        if not product:
            continue

        # Calculate subtotal

        subtotal = product.price * cart_item.quantity

        total_price += subtotal

        # Prepare product response

        items.append(
            CartProductResponse(
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=cart_item.quantity,
                subtotal=subtotal
            )
        )

    # 4. Return complete cart

    return CartResponse(
        cart_id=cart.id,
        user_id=current_user.id,
        items=items,
        total_price=total_price
    )


# ==========================================
# UPDATE CART ITEM QUANTITY
# ==========================================

@router.patch("/update/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # 1. Find user's cart

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:

        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    # 2. Find cart item belonging to user's cart

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    # 3. Find product

    product = db.query(Product).filter(
        Product.id == cart_item.product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # 4. Check stock availability

    if item.quantity > product.quantity:

        raise HTTPException(
            status_code=400,
            detail="Insufficient product stock"
        )

    # 5. Update quantity

    cart_item.quantity = item.quantity

    # 6. Save changes

    db.commit()
    db.refresh(cart_item)

    return cart_item