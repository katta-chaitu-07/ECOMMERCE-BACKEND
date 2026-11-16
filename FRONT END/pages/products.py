
import streamlit as st

from services.product import get_all_products
from services.cart import add_to_cart
from services.auth import is_authenticated


def render_products_page():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("🛍️ Explore Our Collection")

    st.caption(
        "Discover products that match your style and needs."
    )

    st.divider()

    # ==========================================
    # FETCH PRODUCTS
    # ==========================================

    response = get_all_products()

    if not isinstance(response, dict):
        st.error("Invalid response received from the server.")
        return

    if not response.get("success"):
        st.error(
            response.get("error") or "Unable to load products."
        )
        return

    products = response.get("data") or []

    if not isinstance(products, list):
        st.error("Invalid product data received from the server.")
        return

    if not products:
        st.info("No products are available right now.")
        return

    # ==========================================
    # SEARCH AND PRODUCT COUNT
    # ==========================================

    search_col, count_col = st.columns([3, 1])

    with search_col:
        search = st.text_input(
            "🔍 Search Products",
            placeholder="Search by product name...",
            key="product_search"
        )

    with count_col:
        st.metric(
            "Available Products",
            len(products)
        )

    # ==========================================
    # FILTER PRODUCTS
    # ==========================================

    filtered_products = [
        product
        for product in products
        if search.strip().lower() in
        str(product.get("name") or "").lower()
    ]

    if not filtered_products:
        st.warning("No products match your search.")
        return

    st.divider()

    # ==========================================
    # PRODUCT DISPLAY
    # ==========================================

    columns = st.columns(3)

    for index, product in enumerate(filtered_products):

        product_id = product.get("id")
        name = product.get("name") or "Unnamed Product"
        price = float(product.get("price") or 0)
        quantity = int(product.get("quantity") or 0)

        with columns[index % 3]:

            with st.container(border=True):

                st.subheader(f"🛍️ {name}")

                st.title(f"₹{price:,.2f}")

                if quantity > 0:
                    st.success(f"In Stock: {quantity} units")
                else:
                    st.error("Out of Stock")

                st.divider()

                if not is_authenticated():

                    if st.button(
                        "Login to Add to Cart",
                        key=f"login_product_{product_id}",
                        use_container_width=True
                    ):
                        st.session_state.page = "Login"
                        st.rerun()

                elif quantity > 0:

                    if st.button(
                        "🛒 Add to Cart",
                        key=f"add_product_{product_id}",
                        type="primary",
                        use_container_width=True
                    ):

                        result = add_to_cart(product_id)

                        if result.get("success"):
                            st.success(
                                f"{name} added to your cart!"
                            )
                        else:
                            st.error(
                                result.get("error")
                                or "Unable to add product."
                            )

                else:

                    st.button(
                        "Currently Unavailable",
                        key=f"unavailable_{product_id}",
                        disabled=True,
                        use_container_width=True
                    )

    # ==========================================
    # FOOTER
    # ==========================================

    st.divider()

    st.caption(
        "Chaitu Store | Discover More. Choose Better."
    )
