# ============================================
# CHAITU STORE - WEBSITE FOOTER
# ============================================

import streamlit as st


def render_footer():

    st.markdown("---")

    # Divide footer into three sections
    col1, col2, col3 = st.columns([2, 1, 1])

    # ----------------------------------------
    # Section 1: Store Information
    # ----------------------------------------

    with col1:

        st.markdown(
            """
            <h3 style="color:#2563EB;">
                🛍️ CHAITU STORE
            </h3>

            <p style="color:#64748B;">
                Discover Products. Enjoy Shopping.
                <br>
                Your trusted destination for online shopping.
            </p>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------------------
    # Section 2: Quick Links
    # ----------------------------------------

    with col2:

        st.markdown("### Quick Links")

        st.markdown(
            """
            - Home
            - Products
            - Shopping Cart
            - My Orders
            """
        )

    # ----------------------------------------
    # Section 3: Customer Support
    # ----------------------------------------

    with col3:

        st.markdown("### Customer Support")

        st.markdown(
            """
            - Contact Us
            - Help Center
            - Privacy Policy
            - Terms & Conditions
            """
        )

    # ----------------------------------------
    # Copyright Section
    # ----------------------------------------

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#64748B;
            padding:10px;
            font-size:14px;
        ">
            © 2026 Chaitu Store. All Rights Reserved.
            <br>
            Designed with ❤️
        </div>
        """,
        unsafe_allow_html=True
    )