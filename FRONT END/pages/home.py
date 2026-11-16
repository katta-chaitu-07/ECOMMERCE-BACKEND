
import streamlit as st


def render_home_page():

    st.title("🛍️ Welcome to Chaitu Store")

    st.subheader("Your Style. Your Choice. Your Store.")

    st.write(
        "Discover quality products at amazing prices. "
        "Explore our collection and enjoy convenient shopping."
    )

    st.divider()

    st.header("Start Your Shopping Journey")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🛍️ Explore Products",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "Products"
            st.rerun()

    with col2:
        if st.button(
            "🛒 My Shopping Cart",
            use_container_width=True
        ):
            st.session_state.page = "Cart"
            st.rerun()

    st.divider()

    st.header("Why Choose Chaitu Store?")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("✨ Quality")
            st.write("Discover products for your everyday needs.")

    with col2:
        with st.container(border=True):
            st.subheader("🔐 Secure Shopping")
            st.write("Enjoy secure account authentication.")

    with col3:
        with st.container(border=True):
            st.subheader("📦 Your Orders")
            st.write("View your shopping and order history.")

    st.divider()

    st.header("Discover More. Choose Better.")

    st.write(
        "A shopping experience built around simplicity, "
        "convenience and your choices."
    )

    st.caption(
        "© 2026 Chaitu Store | Built with passion and technology."
    )
