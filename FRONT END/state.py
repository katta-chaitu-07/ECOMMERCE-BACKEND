
# ============================================
# CHAITU STORE - SESSION STATE MANAGEMENT
# ============================================

import streamlit as st


def initialize_session_state():

    # ----------------------------------------
    # 1. Shopping Cart
    # ----------------------------------------

    if "cart" not in st.session_state:
        st.session_state.cart = []


    # ----------------------------------------
    # 2. Current Page
    # ----------------------------------------

    if "page" not in st.session_state:
        st.session_state.page = "Home"


    # ----------------------------------------
    # 3. Authentication Token
    # ----------------------------------------

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    # Backward compatibility with services
    if "token" not in st.session_state:
        st.session_state.token = None


    # ----------------------------------------
    # 4. Authentication Status
    # ----------------------------------------

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


    # ----------------------------------------
    # 5. Logged-in User Information
    # ----------------------------------------

    if "user" not in st.session_state:
        st.session_state.user = None


    # ----------------------------------------
    # 6. Registration Status
    # ----------------------------------------

    if "registration_success" not in st.session_state:
        st.session_state.registration_success = False


    # ----------------------------------------
    # 7. Product Search
    # ----------------------------------------

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""


    # ----------------------------------------
    # 8. Product Category
    # ----------------------------------------

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"


    # ----------------------------------------
    # 9. Price Filters
    # ----------------------------------------

    if "min_price" not in st.session_state:
        st.session_state.min_price = 0

    if "max_price" not in st.session_state:
        st.session_state.max_price = None


    # ----------------------------------------
    # 10. Selected Product
    # ----------------------------------------

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None


    # ----------------------------------------
    # 11. Selected Order
    # ----------------------------------------

    if "selected_order_id" not in st.session_state:
        st.session_state.selected_order_id = None


    # ----------------------------------------
    # 12. Checkout Confirmation
    # ----------------------------------------

    if "checkout_success_order" not in st.session_state:
        st.session_state.checkout_success_order = None
