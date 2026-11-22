
from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from APP.database.dependencies import get_db
from APP.security.dependencies import get_current_user

from APP.models.user import User
from APP.models.cart import Cart
from APP.models.cart_item import CartItem
from APP.models.product import Product
from APP.models.order import Order
from APP.models.order_item import OrderItem


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# --------------------------------------------------
# 1. CHECKOUT - Create a new order from the cart
# --------------------------------------------------

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get the logged-in user's cart and its products
    cart = (
        db.query(Cart)
        .options(
            joinedload(Cart.items).joinedload(CartItem.product)
        )
        .filter(Cart.user_id == current_user.id)
        .first()
    )

    # Check whether the cart exists
    if cart is None or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty."
        )

    order_items_data = []
    total_amount = Decimal("0.00")

    # Validate products and calculate the total
    for cart_item in cart.items:

        product = cart_item.product

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A product in your cart no longer exists."
            )

        if cart_item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity for {product.name}."
            )

        if cart_item.quantity > product.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for {product.name}. "
                    f"Available: {product.quantity}."
                )
            )

        unit_price = Decimal(
            str(product.price)
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        subtotal = unit_price * cart_item.quantity

        total_amount += subtotal

        order_items_data.append({
            "product": product,
            "quantity": cart_item.quantity,
            "unit_price": unit_price
        })

    total_amount = total_amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    try:
        # Create the main order
        new_order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status="pending"
        )

        db.add(new_order)

        # Generate the order ID before creating order items
        db.flush()

        response_items = []

        # Create individual order items
        for item_data in order_items_data:

            product = item_data["product"]
            quantity = item_data["quantity"]
            unit_price = item_data["unit_price"]

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price
            )

            db.add(order_item)

            # Reduce product stock
            product.quantity -= quantity

            response_items.append({
                "product_id": product.id,
                "product_name": product.name,
                "quantity": quantity,
                "unit_price": float(unit_price),
                "subtotal": float(unit_price * quantity)
            })

        # Empty the cart after successful order creation
        for cart_item in list(cart.items):
            db.delete(cart_item)

        # Save everything in the database
        db.commit()

        db.refresh(new_order)

        return {
            "message": "Order placed successfully.",
            "order_id": new_order.id,
            "status": new_order.status,
            "total_amount": float(total_amount),
            "items": response_items
        }

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Checkout failed. Please try again."
        )


# --------------------------------------------------
# 2. GET MY ORDERS - Retrieve logged-in user's orders
# --------------------------------------------------

@router.get("/")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "order_id": order.id,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "created_at": (
                order.created_at.isoformat()
                if order.created_at else None
            )
        }
        for order in orders
    ]


# --------------------------------------------------
# 3. GET ORDER BY ID - Retrieve one specific order
# --------------------------------------------------

@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    items = []

    for item in order.items:

        items.append({
            "product_id": item.product_id,
            "product_name": (
                item.product.name
                if item.product else "Unavailable product"
            ),
            "quantity": item.quantity,
            "unit_price": float(item.unit_price),
            "subtotal": float(
                item.unit_price * item.quantity
            )
        })

    return {
        "order_id": order.id,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "created_at": (
            order.created_at.isoformat()
            if order.created_at else None
        ),
        "items": items
    }
