
# ============================================
# CHAITU STORE - HOME PAGE
# ============================================

import streamlit as st

from services.auth import is_authenticated


def render_home_page():

    # ----------------------------------------
    # 1. WELCOME SECTION
    # ----------------------------------------

    st.title("🛍️ Welcome to Chaitu Store")

    st.subheader("Your Style. Your Choice. Your Store.")

    st.write(
        "Discover quality products at amazing prices. "
        "Explore our collection and enjoy a simple, "
        "convenient shopping experience."
    )

    # Personalized greeting
    user = st.session_state.get("user")

    if is_authenticated() and user:

        st.success(
            f"Welcome back, {user.get('name', 'Customer')}! "
            "Happy shopping."
        )

    st.divider()

    # ----------------------------------------
    # 2. MAIN SHOPPING ACTIONS
    # ----------------------------------------

    st.header("Start Your Shopping Journey")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🛍️ Explore Products")

        st.write(
            "Browse our available products and find what you need."
        )

        if st.button(
            "Explore Products",
            key="home_explore_products",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = "Products"
            st.rerun()

    with col2:

        st.subheader("🛒 Shopping Cart")

        st.write(
            "Review your selected products and manage quantities."
        )

        if st.button(
            "View My Cart",
            key="home_view_cart",
            use_container_width=True
        ):

            st.session_state.page = "Cart"
            st.rerun()

    st.divider()

    # ----------------------------------------
    # 3. STORE FEATURES
    # ----------------------------------------

    st.header("Why Choose Chaitu Store?")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader("✨ Quality")

            st.write(
                "Discover products selected for your everyday needs."
            )

    with col2:

        with st.container(border=True):

            st.subheader("🔐 Secure Shopping")

            st.write(
                "Access your account with secure authentication."
            )

    with col3:

        with st.container(border=True):

            st.subheader("📦 Order Tracking")

            st.write(
                "Access your order history and review previous purchases."
            )

    st.divider()

    # ----------------------------------------
    # 4. ACCOUNT ACTIONS
    # ----------------------------------------

    st.header("Your Account")

    if is_authenticated():

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📦 My Orders",
                key="home_my_orders",
                use_container_width=True
            ):

                st.session_state.page = "Orders"
                st.rerun()

        with col2:

            if st.button(
                "🛒 Continue Shopping",
                key="home_continue_shopping",
                use_container_width=True
            ):

                st.session_state.page = "Products"
                st.rerun()

    else:

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🔐 Login",
                key="home_login",
                use_container_width=True
            ):

                st.session_state.page = "Login"
                st.rerun()

        with col2:

            if st.button(
                "📝 Create Account",
                key="home_register",
                use_container_width=True
            ):

                st.session_state.page = "Register"
                st.rerun()

    st.divider()

    # ----------------------------------------
    # 5. FOOTER
    # ----------------------------------------

    st.caption(
        "© 2026 Chaitu Store | Built with passion and technology."
    )
