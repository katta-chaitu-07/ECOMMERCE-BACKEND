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