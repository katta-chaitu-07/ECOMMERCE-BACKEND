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


    # ----------------------------------------
    # 4. Logged-in User Information
    # ----------------------------------------

    if "user" not in st.session_state:
        st.session_state.user = None


    # ----------------------------------------
    # 5. Registration Status
    # ----------------------------------------

    if "registration_success" not in st.session_state:
        st.session_state.registration_success = False


    # ----------------------------------------
    # 6. Product Search
    # ----------------------------------------

    if "search_query" not in st.session_state:
        st.session_state.search_query = ""


    # ----------------------------------------
    # 7. Product Category
    # ----------------------------------------

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"


    # ----------------------------------------
    # 8. Price Filter
    # ----------------------------------------

    if "min_price" not in st.session_state:
        st.session_state.min_price = 0


    if "max_price" not in st.session_state:
        st.session_state.max_price = None


    # ----------------------------------------
    # 9. Selected Product
    # ----------------------------------------

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None