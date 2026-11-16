
import streamlit as st
from pathlib import Path

from state import initialize_session_state

from components.navbar import render_navbar

from pages.home import render_home_page
from pages.products import render_products_page
from pages.register import render_register_page

from services.auth import login, logout, is_authenticated
from services.cart import (
    get_cart,
    update_cart_item,
    remove_from_cart
)
from services.order import checkout, get_orders


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Chaitu Store | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# LOAD WEBSITE STYLESHEET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


def load_styles():

    css_path = BASE_DIR / "styles" / "style.css"

    if not css_path.is_file():
        st.error(f"Website stylesheet not found: {css_path}")
        return

    try:
        css = css_path.read_text(encoding="utf-8")

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    except OSError as error:
        st.error(f"Unable to load stylesheet: {error}")


# ==========================================
# LOGIN PAGE
# ==========================================

def render_login_page():

    st.title("Welcome Back 👋")
    st.write("Log in to continue shopping at Chaitu Store.")

    with st.container(border=True):

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button("Login", use_container_width=True):

            if not email or not password:
                st.warning("Please enter your email and password.")
                return

            response = login(email, password)

            if response.get("success"):

                st.success("Login successful!")
                st.session_state.page = "Home"
                st.rerun()

            else:
                st.error(
                    response.get("error", "Login failed.")
                )

    st.write("Don't have an account?")

    if st.button("Create an Account"):
        st.session_state.page = "Register"
        st.rerun()


# ==========================================
# CART PAGE
# ==========================================

def render_cart_page():

    st.title("🛒 Your Shopping Cart")

    if not is_authenticated():
        st.warning("Please log in to view your cart.")

        if st.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()

        return

    response = get_cart()

    if not response.get("success"):
        st.error(response.get("error", "Unable to load cart."))
        return

    cart_data = response.get("data") or {}

    items = cart_data.get("items", [])

    if not items:
        st.info("Your shopping cart is empty.")

        if st.button("Explore Products"):
            st.session_state.page = "Products"
            st.rerun()

        return

    total_amount = 0

    for item in items:

        product_id = item.get("product_id")
        product_name = item.get("product_name", "Product")
        price = float(item.get("unit_price", 0))
        quantity = int(item.get("quantity", 1))
        subtotal = float(item.get("subtotal", price * quantity))

        total_amount += subtotal

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.subheader(product_name)
                st.write(f"Price: ₹{price:,.2f}")

            with col2:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=quantity,
                    step=1,
                    key=f"quantity_{product_id}"
                )

                if new_quantity != quantity:

                    if st.button(
                        "Update",
                        key=f"update_{product_id}"
                    ):

                        result = update_cart_item(
                            product_id,
                            new_quantity
                        )

                        if result.get("success"):
                            st.rerun()
                        else:
                            st.error(
                                result.get("error", "Update failed.")
                            )

            with col3:

                st.write(f"Subtotal: ₹{subtotal:,.2f}")

                if st.button(
                    "Remove",
                    key=f"remove_{product_id}"
                ):

                    result = remove_from_cart(product_id)

                    if result.get("success"):
                        st.rerun()
                    else:
                        st.error(
                            result.get("error", "Remove failed.")
                        )

    st.divider()

    st.subheader(f"Total: ₹{total_amount:,.2f}")

    if st.button("Proceed to Checkout", use_container_width=True):

        result = checkout()

        if result.get("success"):

            st.success("Order placed successfully! 🎉")

            st.session_state.page = "Orders"
            st.rerun()

        else:
            st.error(
                result.get("error", "Checkout failed.")
            )


# ==========================================
# ORDER HISTORY PAGE
# ==========================================

def render_orders_page():

    st.title("📦 My Orders")

    if not is_authenticated():

        st.warning("Please log in to view your orders.")

        if st.button("Login"):
            st.session_state.page = "Login"
            st.rerun()

        return

    response = get_orders()

    if not response.get("success"):
        st.error(
            response.get("error", "Unable to load orders.")
        )
        return

    orders = response.get("data") or []

    if not orders:
        st.info("You haven't placed any orders yet.")
        return

    for order in orders:

        order_id = order.get("id", order.get("order_id", "N/A"))

        with st.expander(f"Order #{order_id}"):

            st.write(
                f"**Status:** {order.get('status', 'N/A')}"
            )

            st.write(
                f"**Total:** ₹{float(order.get('total_amount', 0)):,.2f}"
            )

            items = order.get("items", [])

            if items:

                st.write("### Ordered Products")

                for item in items:

                    product_name = item.get(
                        "product_name",
                        item.get("product", {}).get("name", "Product")
                    )

                    st.write(
                        f"- {product_name} | "
                        f"Quantity: {item.get('quantity', 0)}"
                    )


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    initialize_session_state()

    load_styles()

    render_navbar()

    st.divider()

    current_page = st.session_state.get("page", "Home")

    if current_page == "Home":

        render_home_page()

    elif current_page == "Products":

        render_products_page()

    elif current_page == "Login":

        render_login_page()

    elif current_page == "Register":

        render_register_page()

    elif current_page == "Cart":

        render_cart_page()

    elif current_page == "Orders":

        render_orders_page()

    else:

        st.session_state.page = "Home"
        st.rerun()


if __name__ == "__main__":
    main()
