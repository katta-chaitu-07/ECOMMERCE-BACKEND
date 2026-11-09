import streamlit as st

# Import product service
from services.product import get_all_products


# ==========================================
# HOMEPAGE HERO SECTION
# ==========================================

def render_hero():

    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #1e3a8a, #2563eb);
            padding: 55px 40px;
            border-radius: 15px;
            color: white;
            margin-bottom: 30px;
        ">

            <h1 style="font-size: 42px;">
                Welcome to Chaitu Store
            </h1>

            <p style="font-size: 19px;">
                Discover quality products at amazing prices.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# PRODUCT SECTION
# ==========================================

def render_products():

    st.markdown("## Explore Our Products")

    # Fetch products from FastAPI
    response = get_all_products()

    # Check API response
    if not response["success"]:

        st.error(
            f"Unable to load products: {response['error']}"
        )

        return

    products = response["data"]

    # Check whether products exist
    if not products:

        st.info("No products are currently available.")

        return

    # Product search
    search_query = st.text_input(
        "🔍 Search Products",
        placeholder="Search for laptops, mobiles..."
    )

    # Filter products
    if search_query:

        products = [
            product for product in products
            if search_query.lower() in product["name"].lower()
        ]

    if not products:

        st.warning("No matching products found.")

        return

    # Display products in three columns
    columns = st.columns(3)

    for index, product in enumerate(products):

        with columns[index % 3]:

            with st.container(border=True):

                st.markdown(
                    f"### {product['name']}"
                )

                st.markdown(
                    f"**Product ID:** {product['id']}"
                )

                st.markdown(
                    f"### ₹{product['price']:,.2f}"
                )

                st.caption(
                    f"Available Quantity: {product['quantity']}"
                )

                if product["quantity"] > 0:

                    st.success("In Stock")

                else:

                    st.error("Out of Stock")


# ==========================================
# HOMEPAGE MAIN FUNCTION
# ==========================================

def render_home_page():

    # Display hero section
    render_hero()

    # Display product section
    render_products()