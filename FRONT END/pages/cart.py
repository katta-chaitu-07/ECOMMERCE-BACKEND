
# ============================================
# CHAITU STORE - SHOPPING CART PAGE
# ============================================

import streamlit as st

from services.cart import (
    get_cart,
    update_cart_item,
    remove_from_cart
)

from services.order import checkout
from services.auth import is_authenticated


def render_cart_page():

    # ==========================================
    # 1. PAGE HEADER
    # ==========================================

    st.title("🛒 My Shopping Cart")

    st.caption(
        "Review your selected products before checkout."
    )

    st.divider()

    # ==========================================
    # 2. AUTHENTICATION CHECK
    # ==========================================

    if not is_authenticated():

        st.warning("Please log in to view your shopping cart.")

        if st.button(
            "🔐 Go to Login",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = "Login"
            st.rerun()

        return

    # ==========================================
    # 3. CHECKOUT SUCCESS CONFIRMATION
    # ==========================================

    completed_order = st.session_state.get(
        "checkout_success_order"
    )

    if completed_order:

        st.success(
            "🎉 Your order has been placed successfully!"
        )

        st.subheader(
            f"Order #{completed_order.get('order_id', 'N/A')}"
        )

        try:
            total_amount = float(
                completed_order.get("total_amount", 0)
            )
        except (TypeError, ValueError):
            total_amount = 0.0

        st.write(
            f"**Total Amount:** ₹{total_amount:,.2f}"
        )

        st.write(
            f"**Status:** "
            f"{str(completed_order.get('status', 'Processing')).title()}"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📦 View My Orders",
                use_container_width=True
            ):

                st.session_state.pop(
                    "checkout_success_order",
                    None
                )

                st.session_state.page = "Orders"
                st.rerun()

        with col2:

            if st.button(
                "🛍️ Continue Shopping",
                use_container_width=True
            ):

                st.session_state.pop(
                    "checkout_success_order",
                    None
                )

                st.session_state.page = "Products"
                st.rerun()

        return

    # ==========================================
    # 4. FETCH CART DATA
    # ==========================================

    with st.spinner("Loading your cart..."):

        response = get_cart()

    if not isinstance(response, dict):

        st.error("Invalid response received from the server.")
        return

    if not response.get("success"):

        st.error(
            response.get("error", "Unable to load your cart.")
        )

        return

    cart_data = response.get("data") or {}

    if not isinstance(cart_data, dict):

        st.error("Invalid cart data received.")
        return

    items = cart_data.get("items") or []

    # ==========================================
    # 5. EMPTY CART
    # ==========================================

    if not items:

        st.info("🛒 Your shopping cart is currently empty.")

        if st.button(
            "Explore Products",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = "Products"
            st.rerun()

        return

    # ==========================================
    # 6. CART ITEMS
    # ==========================================

    st.subheader("Your Cart Items")

    for item in items:

        if not isinstance(item, dict):
            continue

        product_id = item.get("product_id")
        product_name = item.get(
            "product_name",
            "Unnamed Product"
        )

        try:

            quantity = int(item.get("quantity", 1))
            unit_price = float(item.get("unit_price", 0))
            subtotal = float(
                item.get("subtotal", quantity * unit_price)
            )

        except (TypeError, ValueError):

            st.error(
                f"Invalid cart item data for {product_name}."
            )

            continue

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.subheader(f"🛍️ {product_name}")

                st.write(
                    f"Unit Price: ₹{unit_price:,.2f}"
                )

                st.write(
                    f"Quantity: {quantity}"
                )

                st.write(
                    f"Subtotal: ₹{subtotal:,.2f}"
                )

            with col2:

                st.write("**Manage Item**")

                # Increase quantity
                if st.button(
                    "➕",
                    key=f"increase_{product_id}",
                    use_container_width=True
                ):

                    result = update_cart_item(
                        product_id,
                        quantity + 1
                    )

                    if result.get("success"):
                        st.rerun()

                    else:
                        st.error(
                            result.get(
                                "error",
                                "Unable to update quantity."
                            )
                        )

                # Decrease quantity
                if st.button(
                    "➖",
                    key=f"decrease_{product_id}",
                    disabled=(quantity <= 1),
                    use_container_width=True
                ):

                    result = update_cart_item(
                        product_id,
                        quantity - 1
                    )

                    if result.get("success"):
                        st.rerun()

                    else:
                        st.error(
                            result.get(
                                "error",
                                "Unable to update quantity."
                            )
                        )

                # Remove product
                if st.button(
                    "🗑️ Remove",
                    key=f"remove_{product_id}",
                    use_container_width=True
                ):

                    result = remove_from_cart(product_id)

                    if result.get("success"):

                        st.success(
                            f"{product_name} removed from cart."
                        )

                        st.rerun()

                    else:

                        st.error(
                            result.get(
                                "error",
                                "Unable to remove product."
                            )
                        )

    # ==========================================
    # 7. CART TOTAL
    # ==========================================

    st.divider()

    try:

        total_amount = float(
            cart_data.get("total_amount", 0)
        )

    except (TypeError, ValueError):

        st.error("Invalid cart total received.")
        return

    st.subheader("Order Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Total Amount**")

    with col2:
        st.markdown(
            f"### ₹{total_amount:,.2f}"
        )

    st.divider()

    # ==========================================
    # 8. CHECKOUT
    # ==========================================

    if st.button(
        "💳 Proceed to Checkout",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Processing your order..."):

            response = checkout()

        if response.get("success"):

            order_data = response.get("data") or {}

            if not isinstance(order_data, dict):

                st.error("Invalid order confirmation received.")

            else:

                st.session_state.checkout_success_order = order_data

                st.rerun()

        else:

            st.error(
                response.get(
                    "error",
                    "Checkout failed. Please try again."
                )
            )

    # ==========================================
    # 9. FOOTER
    # ==========================================

    st.divider()

    st.caption(
        "Chaitu Store | Thank you for shopping with us!"
    )
