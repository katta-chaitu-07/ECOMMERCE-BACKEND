
# ============================================
# CHAITU STORE - PRODUCTS PAGE
# ============================================

import streamlit as st

from services.product import get_all_products
from services.cart import add_to_cart
from services.auth import is_authenticated


# ============================================
# RENDER PRODUCTS PAGE
# ============================================

def render_products_page():

    # ----------------------------------------
    # 1. PAGE HEADER
    # ----------------------------------------

    st.title("🛍️ Explore Our Collection")

    st.caption(
        "Discover products that match your style and needs."
    )

    st.divider()

    # ----------------------------------------
    # 2. FETCH PRODUCTS
    # ----------------------------------------

    with st.spinner("Loading products..."):

        response = get_all_products()

    if not isinstance(response, dict):

        st.error("Invalid response received from the server.")
        st.write("DEBUG RESPONSE:", response)
        return

    if not response.get("success"):

        st.error(
            response.get("error") or "Unable to load products."
        )

        st.write("DEBUG RESPONSE:", response)
        return

    products = response.get("data")

    if not isinstance(products, list):

        st.error("Invalid product data received.")
        st.write("DEBUG DATA:", products)
        return

    if not products:

        st.info("No products available right now.")
        return

    # ----------------------------------------
    # 3. SEARCH AND SORT
    # ----------------------------------------

    search_col, sort_col = st.columns([2, 2])

    with search_col:

        search = st.text_input(
            "🔍 Search Products",
            placeholder="Search by product name...",
            key="search_query"
        )

    with sort_col:

        sort_option = st.selectbox(
            "Sort Products",
            [
                "Default",
                "Price: Low to High",
                "Price: High to Low",
                "Name: A to Z"
            ],
            key="product_sort"
        )

    # ----------------------------------------
    # 4. FILTER PRODUCTS
    # ----------------------------------------

    filtered_products = []

    for product in products:

        if not isinstance(product, dict):
            continue

        name = str(product.get("name", ""))

        if search.strip().lower() in name.lower():

            filtered_products.append(product)

    # ----------------------------------------
    # 5. SORT PRODUCTS
    # ----------------------------------------

    if sort_option == "Price: Low to High":

        filtered_products.sort(
            key=lambda p: float(p.get("price", 0))
        )

    elif sort_option == "Price: High to Low":

        filtered_products.sort(
            key=lambda p: float(p.get("price", 0)),
            reverse=True
        )

    elif sort_option == "Name: A to Z":

        filtered_products.sort(
            key=lambda p: str(p.get("name", "")).lower()
        )

    # ----------------------------------------
    # 6. PRODUCT COUNT
    # ----------------------------------------

    st.metric(
        "Products Found",
        len(filtered_products)
    )

    if not filtered_products:

        st.warning("No products match your search.")
        return

    st.divider()

    # ----------------------------------------
    # 7. DISPLAY PRODUCT CARDS
    # ----------------------------------------

    columns = st.columns(3)

    for index, product in enumerate(filtered_products):

        try:

            product_id = int(product["id"])
            name = str(product["name"])
            price = float(product["price"])
            quantity = int(product["quantity"])

            image_url = product.get("image_url")

            if price < 0 or quantity < 0:
                raise ValueError("Invalid price or stock.")

        except (KeyError, TypeError, ValueError) as error:

            st.warning(f"Skipping invalid product: {error}")
            continue

        # ------------------------------------
        # DEBUG: CHECK IMAGE URL
        # ------------------------------------

        with columns[index % 3]:

            with st.container(border=True):

                st.write("DEBUG IMAGE URL:", image_url)

                # --------------------------------
                # 8. DISPLAY PRODUCT IMAGE
                # --------------------------------

                if image_url and str(image_url).strip():

                    try:

                        st.image(
                            str(image_url).strip(),
                            use_container_width=True
                        )

                    except Exception as error:

                        st.warning("Unable to display product image.")

                        st.caption(
                            f"Image error: {error}"
                        )

                        st.image(
                            "https://placehold.co/600x400?text=Image+Unavailable",
                            use_container_width=True
                        )

                else:

                    st.image(
                        "https://placehold.co/600x400?text=No+Product+Image",
                        use_container_width=True
                    )

                # --------------------------------
                # 9. PRODUCT INFORMATION
                # --------------------------------

                st.markdown(f"### 🛍️ {name}")

                st.markdown(
                    f"## ₹{price:,.2f}"
                )

                st.caption(f"Product ID: {product_id}")

                if quantity > 0:

                    st.success(
                        f"📦 In Stock: {quantity} units"
                    )

                else:

                    st.error("Out of Stock")

                st.divider()

                # --------------------------------
                # 10. CART ACTIONS
                # --------------------------------

                if not is_authenticated():

                    if st.button(
                        "🔐 Login to Add to Cart",
                        key=f"login_product_{product_id}",
                        use_container_width=True
                    ):

                        st.session_state.page = "Login"
                        st.rerun()

                elif quantity > 0:

                    selected_quantity = st.number_input(
                        "Select Quantity",
                        min_value=1,
                        max_value=quantity,
                        value=1,
                        step=1,
                        key=f"quantity_{product_id}"
                    )

                    if st.button(
                        "🛒 Add to Cart",
                        key=f"add_product_{product_id}",
                        type="primary",
                        use_container_width=True
                    ):

                        with st.spinner("Adding to cart..."):

                            result = add_to_cart(
                                product_id,
                                quantity=int(selected_quantity)
                            )

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

    # ----------------------------------------
    # 11. FOOTER
    # ----------------------------------------

    st.divider()

    st.caption(
        "Chaitu Store | Discover More. Choose Better."
    )
