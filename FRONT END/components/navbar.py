
import streamlit as st

from services.auth import is_authenticated, logout


def navigate_to(page):
    st.session_state.page = page
    st.rerun()


def render_navbar():

    # Store branding
    st.title("🛍️ CHAITU STORE")
    st.caption("YOUR STYLE. YOUR CHOICE. YOUR STORE.")

    st.divider()

    # Navigation menu
    if is_authenticated():

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            if st.button("🏠 Home", use_container_width=True):
                navigate_to("Home")

        with col2:
            if st.button("🛍️ Products", use_container_width=True):
                navigate_to("Products")

        with col3:
            if st.button("🛒 Cart", use_container_width=True):
                navigate_to("Cart")

        with col4:
            if st.button("📦 Orders", use_container_width=True):
                navigate_to("Orders")

        with col5:
            if st.button("👤 Account", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()

        with col6:
            if st.button("Logout", use_container_width=True):
                logout()

    else:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("🏠 Home", use_container_width=True):
                navigate_to("Home")

        with col2:
            if st.button("🛍️ Products", use_container_width=True):
                navigate_to("Products")

        with col3:
            if st.button("🔐 Login", use_container_width=True):
                navigate_to("Login")

        with col4:
            if st.button("📝 Register", use_container_width=True):
                navigate_to("Register")

        with col5:
            if st.button("🛒 Cart", use_container_width=True):
                navigate_to("Cart")

    st.divider()
