
import streamlit as st
from pathlib import Path

# ==========================================
# IMPORT SESSION STATE
# ==========================================

from state import initialize_session_state

# ==========================================
# IMPORT COMPONENTS
# ==========================================

from components.navbar import render_navbar

# ==========================================
# IMPORT FRONTEND PAGES
# ==========================================

from pages.home import render_home_page
from pages.products import render_products_page
from pages.login import render_login_page
from pages.register import render_register_page
from pages.cart import render_cart_page
from pages.orders import render_orders_page


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

def load_custom_css():

    css_path = Path(__file__).parent / "styles" / "style.css"

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as file:

            css = file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )


# ==========================================
# PAGE ROUTING
# ==========================================

def render_page():

    current_page = st.session_state.get("page", "Home")

    # HOME PAGE
    if current_page == "Home":

        render_home_page()

    # PRODUCTS PAGE
    elif current_page == "Products":

        render_products_page()

    # LOGIN PAGE
    elif current_page == "Login":

        render_login_page()

    # REGISTRATION PAGE
    elif current_page == "Register":

        render_register_page()

    # SHOPPING CART
    elif current_page == "Cart":

        render_cart_page()

    # ORDER HISTORY
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

    # Initialize session variables
    initialize_session_state()

    # Load website styling
    load_custom_css()

    # Render navigation
    render_navbar()

    # Render selected page
    render_page()


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()
