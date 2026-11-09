# ============================================
# CHAITU STORE - NAVIGATION BAR
# ============================================

import streamlit as st

# Import logout function
from services.auth import logout


def render_navbar():

    # ----------------------------------------
    # CHECK AUTHENTICATION STATUS
    # ----------------------------------------

    is_logged_in = st.session_state.get("access_token") is not None

    # ----------------------------------------
    # CREATE NAVIGATION COLUMNS
    # ----------------------------------------

    col1, col2, col3 = st.columns([2.5, 5, 2.5])

    selected_page = None

    # ----------------------------------------
    # STORE LOGO
    # ----------------------------------------

    with col1:

        st.markdown(
            """
            <h2 style="
                color:#2563EB;
                margin-top:5px;
                font-size:25px;
                font-weight:800;
            ">
                🛍️ CHAITU STORE
            </h2>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------------
    # NAVIGATION BUTTONS
    # ----------------------------------------

    with col2:

        if is_logged_in:

            nav1, nav2, nav3, nav4 = st.columns(4)

            navigation = {
                "Home": nav1,
                "Products": nav2,
                "Cart": nav3,
                "Orders": nav4
            }

        else:

            nav1, nav2, nav3 = st.columns(3)

            navigation = {
                "Home": nav1,
                "Products": nav2,
                "Cart": nav3
            }

        for page, column in navigation.items():

            with column:

                if st.button(
                    page,
                    key=f"nav_{page}",
                    use_container_width=True
                ):

                    selected_page = page

    # ----------------------------------------
    # AUTHENTICATION SECTION
    # ----------------------------------------

    with col3:

        if is_logged_in:

            user = st.session_state.get("user") or {}

            user_name = user.get("name", "Account")

            st.caption(f"👤 {user_name}")

            if st.button(
                "Logout",
                key="logout_button",
                use_container_width=True
            ):

                logout()

        else:

            auth_col1, auth_col2 = st.columns(2)

            with auth_col1:

                if st.button(
                    "Login",
                    key="login_button",
                    use_container_width=True
                ):

                    selected_page = "Login"

            with auth_col2:

                if st.button(
                    "Register",
                    key="register_button",
                    use_container_width=True
                ):

                    selected_page = "Register"

    # ----------------------------------------
    # UPDATE CURRENT PAGE
    # ----------------------------------------

    if selected_page:

        st.session_state.page = selected_page

        st.rerun()

    # ----------------------------------------
    # NAVIGATION DIVIDER
    # ----------------------------------------

    st.divider()

    return st.session_state.page