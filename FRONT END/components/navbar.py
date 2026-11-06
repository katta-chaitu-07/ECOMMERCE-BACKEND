# ============================================
# CHAITU STORE - NAVIGATION BAR
# ============================================

import streamlit as st


def render_navbar():

    # ----------------------------------------
    # Create navigation columns
    # ----------------------------------------

    col1, col2, col3 = st.columns([2, 5, 2])

    # ----------------------------------------
    # Store Logo
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
    # Navigation Buttons
    # ----------------------------------------

    with col2:

        nav1, nav2, nav3, nav4, nav5 = st.columns(5)

        navigation = {
            "Home": nav1,
            "Products": nav2,
            "Cart": nav3,
            "Orders": nav4,
            "Login": nav5
        }

        selected_page = None

        for page, column in navigation.items():

            with column:

                if st.button(page, key=f"nav_{page}"):

                    selected_page = page

    # ----------------------------------------
    # Authentication Section
    # ----------------------------------------

    with col3:

        if st.session_state.access_token:

            if st.button("Logout", key="logout_button"):

                st.session_state.access_token = None
                st.session_state.user = None

                st.session_state.page = "Home"

                st.rerun()

        else:

            if st.button("Register", key="register_button"):

                selected_page = "Register"

    # ----------------------------------------
    # Update Current Page
    # ----------------------------------------

    if selected_page:

        st.session_state.page = selected_page

        st.rerun()

    st.divider()

    return st.session_state.page