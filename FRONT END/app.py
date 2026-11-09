import streamlit as st
from pathlib import Path


# ==========================================
# IMPORTS
# ==========================================

# Initialize session state
from state import initialize_session_state

# Navigation component
from components.navbar import render_navbar

# Homepage
from pages.home import render_home_page

# Registration page
from pages.register import render_register_page

# Authentication services
from services.auth import (
    login,
    logout,
    is_authenticated
)

# Product services
from services.product import (
    get_all_products,
    get_product_by_id,
    search_products,
    filter_products
)


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
# LOAD CUSTOM CSS
# ==========================================

def load_styles():

    """
    Load custom CSS styles from the styles directory.
    """

    css_file = Path(__file__).parent / "styles" / "style.css"

    if css_file.exists():

        with open(css_file, "r", encoding="utf-8") as file:

            css = file.read()

            st.markdown(
                f"<style>{css}</style>",
                unsafe_allow_html=True
            )


# ==========================================
# INITIALIZE APPLICATION
# ==========================================

def initialize_app():

    """
    Initialize application-level session variables.
    """

    initialize_session_state()


# ==========================================
# LOGIN PAGE
# ==========================================

def render_login_page():

    st.title("🔐 Welcome Back")

    st.write("Login to your Chaitu Store account.")

    st.markdown("---")

    # Login form
    with st.form("login_form"):

        # Email
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        # Password
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        # Submit button
        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            # Validate fields
            if not email or not password:

                st.error(
                    "Please enter both email and password."
                )

            else:

                # Authenticate user
                with st.spinner("Authenticating..."):

                    response = login(
                        email=email.strip(),
                        password=password
                    )

                # Check login response
                if response.get("success"):

                    st.success("Login successful!")

                    st.session_state.page = "Home"

                    st.rerun()

                else:

                    st.error(
                        response.get("error", "Login failed.")
                    )

    # Registration navigation
    st.write("Don't have an account?")

    if st.button("Create New Account"):

        st.session_state.page = "Register"

        st.rerun()


# ==========================================
# PRODUCTS PAGE
# ==========================================

def render_products_page():

    st.title("🛍️ Explore Our Products")

    st.write("Discover products available at Chaitu Store.")

    st.markdown("---")

    # Product search
    search_query = st.text_input(
        "🔍 Search Products",
        placeholder="Search by product name..."
    )

    # Retrieve products from backend
    response = get_all_products()

    if not response["success"]:

        st.error(
            f"Unable to load products: {response['error']}"
        )

        return

    products = response["data"]

    if not products:

        st.info("No products are currently available.")

        return

    # Search filter
    if search_query:

        products = [
            product for product in products
            if search_query.lower() in product["name"].lower()
        ]

    # Price filter
    st.subheader("Filter Products")

    min_available = min(
        product["price"] for product in response["data"]
    )

    max_available = max(
        product["price"] for product in response["data"]
    )

    min_price, max_price = st.slider(
        "Select Price Range",
        min_value=int(min_available),
        max_value=max(
            int(max_available),
            int(min_available) + 1
        ),
        value=(
            int(min_available),
            max(
                int(max_available),
                int(min_available) + 1
            )
        )
    )

    products = [
        product for product in products
        if min_price <= product["price"] <= max_price
    ]

    st.markdown("---")

    st.subheader(
        f"Available Products ({len(products)})"
    )

    # Display products in three columns
    columns = st.columns(3)

    for index, product in enumerate(products):

        with columns[index % 3]:

            with st.container(border=True):

                st.subheader(product["name"])

                st.markdown(
                    f"### ₹{product['price']:,.2f}"
                )

                st.write(
                    f"Available Quantity: {product['quantity']}"
                )

                # Add product to cart
                if st.button(
                    "🛒 Add to Cart",
                    key=f"add_product_{product['id']}",
                    use_container_width=True,
                    disabled=product["quantity"] <= 0
                ):

                    cart = st.session_state.cart

                    # Check whether product already exists
                    existing_item = next(
                        (
                            item for item in cart
                            if item["id"] == product["id"]
                        ),
                        None
                    )

                    if existing_item:

                        if existing_item["quantity"] < product["quantity"]:

                            existing_item["quantity"] += 1

                            st.success("Cart quantity updated!")

                        else:

                            st.warning(
                                "Maximum available quantity reached."
                            )

                    else:

                        cart.append({
                            "id": product["id"],
                            "name": product["name"],
                            "price": product["price"],
                            "quantity": 1
                        })

                        st.success("Product added to cart!")

                    st.rerun()


# ==========================================
# SHOPPING CART PAGE
# ==========================================

def render_cart_page():

    st.title("🛒 Your Shopping Cart")

    cart = st.session_state.cart

    if not cart:

        st.info("Your shopping cart is empty.")

        if st.button("Continue Shopping"):

            st.session_state.page = "Products"

            st.rerun()

        return

    total_amount = 0

    # Display cart items
    for index, item in enumerate(cart):

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:

            st.write(f"**{item['name']}**")

        with col2:

            st.write(f"₹{item['price']:,.2f}")

        with col3:

            st.write(f"Qty: {item['quantity']}")

        with col4:

            if st.button(
                "Remove",
                key=f"remove_{item['id']}"
            ):

                cart.pop(index)

                st.rerun()

        total_amount += item["price"] * item["quantity"]

    st.markdown("---")

    st.subheader(
        f"Total Amount: ₹{total_amount:,.2f}"
    )

    # Continue shopping
    if st.button(
        "Continue Shopping",
        use_container_width=True
    ):

        st.session_state.page = "Products"

        st.rerun()

    # Checkout
    if st.button(
        "Proceed to Checkout",
        use_container_width=True
    ):

        if not is_authenticated():

            st.warning(
                "Please log in before proceeding to checkout."
            )

            st.session_state.page = "Login"

            st.rerun()

        else:

            st.info(
                "Checkout functionality will be implemented next."
            )


# ==========================================
# ORDERS PAGE
# ==========================================

def render_orders_page():

    st.title("📦 My Orders")

    # Check authentication
    if not is_authenticated():

        st.warning("Please log in to view your orders.")

        if st.button("Login Now"):

            st.session_state.page = "Login"

            st.rerun()

        return

    st.info(
        "Order management will be implemented in the next phase."
    )


# ==========================================
# PAGE ROUTING
# ==========================================

def render_page():

    """
    Display the page selected by the user.
    """

    current_page = st.session_state.page

    # HOME
    if current_page == "Home":

        render_home_page()

    # PRODUCTS
    elif current_page == "Products":

        render_products_page()

    # LOGIN
    elif current_page == "Login":

        render_login_page()

    # REGISTER
    elif current_page == "Register":

        render_register_page()

    # CART
    elif current_page == "Cart":

        render_cart_page()

    # ORDERS
    elif current_page == "Orders":

        render_orders_page()

    # INVALID PAGE
    else:

        st.error("Page not found.")

        if st.button("Return Home"):

            st.session_state.page = "Home"

            st.rerun()


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    """
    Main entry point of Chaitu Store.
    """

    # Initialize session state
    initialize_app()

    # Load custom CSS
    load_styles()

    # Render navigation bar
    render_navbar()

    # Render selected page
    render_page()


# ==========================================
# APPLICATION EXECUTION
# ==========================================

if __name__ == "__main__":

    main()