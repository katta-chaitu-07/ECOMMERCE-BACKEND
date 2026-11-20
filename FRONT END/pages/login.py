
# ============================================
# CHAITU STORE - LOGIN PAGE
# ============================================

import streamlit as st

from services.auth import login, is_authenticated


def render_login_page():

    st.title("🔐 Welcome Back")
    st.caption("Log in to your Chaitu Store account.")

    # Already logged in
    if is_authenticated():
        st.success("You are already logged in!")

        if st.button("Continue Shopping", use_container_width=True):
            st.session_state.page = "Products"
            st.rerun()

        return

    # Login form
    with st.form("login_form"):

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
            type="primary"
        )

    if submitted:

        if not email.strip() or not password:
            st.warning("Please enter both email and password.")

        else:
            with st.spinner("Logging you in..."):

                response = login(
                    email=email,
                    password=password
                )

            if response.get("success"):

                st.success("Login successful!")

                st.session_state.page = "Home"
                st.rerun()

            else:
                st.error(
                    response.get("error", "Login failed. Please try again.")
                )

    st.divider()

    st.write("Don't have an account?")

    if st.button("Create New Account", use_container_width=True):
        st.session_state.page = "Register"
        st.rerun()
