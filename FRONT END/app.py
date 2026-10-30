
import streamlit as st
import requests
import html

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="Chaitu Store | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/products/"

# ---------------- SESSION STATE ----------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "search" not in st.session_state:
    st.session_state.search = ""

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Navigation */

.navbar {
    background: #101828;
    padding: 22px 30px;
    border-radius: 14px;
    color: white;
    margin-bottom: 28px;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.brand span {
    color: #fbbf24;
}

.nav-info {
    color: #d0d5dd;
    font-size: 13px;
}

/* Hero */

.hero {
    background: linear-gradient(115deg, #172554, #2563eb);
    padding: 55px 45px;
    border-radius: 20px;
    color: white;
    margin-bottom: 35px;
}

.hero-tag {
    background: rgba(255,255,255,0.16);
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 12px;
}

.hero h1 {
    font-size: 40px;
    line-height: 1.2;
    font-weight: 800;
    margin-top: 22px;
}

.hero p {
    color: #dbeafe;
    font-size: 15px;
    max-width: 500px;
}

/* Section headings */

.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #101828;
    margin-top: 30px;
}

.section-subtitle {
    color: #667085;
    font-size: 13px;
    margin-bottom: 20px;
}

/* Product cards */

.product-card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #eaecf0;
    margin-bottom: 8px;
    min-height: 145px;
    transition: 0.2s ease;
}

.product-card:hover {
    border-color: #2563eb;
    box-shadow: 0 8px 25px rgba(16,24,40,0.08);
    transform: translateY(-3px);
}

.product-icon {
    height: 65px;
    background: #eff4ff;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 32px;
    margin-bottom: 15px;
}

.product-name {
    font-size: 15px;
    font-weight: 700;
    color: #101828;
    margin-bottom: 8px;
}

.product-price {
    color: #2563eb;
    font-size: 19px;
    font-weight: 800;
}

.product-stock {
    color: #667085;
    font-size: 12px;
}

/* Buttons */

.stButton > button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
    height: 42px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
    border: none;
}

/* Search input */

.stTextInput input {
    border-radius: 10px;
    border: 1px solid #d0d5dd;
    background: white;
}

</style>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------

cart_count = sum(
    item["quantity"]
    for item in st.session_state.cart.values()
)

st.markdown(f"""
<div class="navbar">
    <div class="brand">
        CHAITU<span>STORE.</span>
    </div>
    <div class="nav-info">
        YOUR ONE-STOP SHOPPING DESTINATION
    </div>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([5, 1, 1])

with nav1:
    st.caption("HOME  /  SHOP  /  PRODUCTS")

with nav2:
    st.write("👤 Account")

with nav3:
    st.write(f"🛒 Cart ({cart_count})")


# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero">
    <span class="hero-tag">WELCOME TO CHAITU STORE</span>

    <h1>Discover Products.<br>
    Enjoy Better Shopping.</h1>

    <p>
    Explore our collection of products and find
    everything you need in one convenient place.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- SEARCH ----------------

st.markdown(
    '<div class="section-title">Find Your Products</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search",
    placeholder="Search for products...",
    label_visibility="collapsed"
)


# ---------------- FETCH PRODUCTS ----------------

st.markdown("""
<div class="section-title">Featured Products</div>
<div class="section-subtitle">
Explore our available products
</div>
""", unsafe_allow_html=True)

try:

    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()

    products = response.json()

    if not isinstance(products, list):
        st.error("Invalid product data received.")
        st.stop()

    filtered_products = [
        product for product in products
        if search.lower() in product["name"].lower()
    ]

    if not filtered_products:

        st.info("No products available.")

    else:

        cols = st.columns(3)

        for index, product in enumerate(filtered_products):

            with cols[index % 3]:

                name = html.escape(str(product["name"]))
                price = float(product["price"])
                quantity = int(product["quantity"])

                st.markdown(f"""
                <div class="product-card">

                    <div class="product-icon">
                        🛍️
                    </div>

                    <div class="product-name">
                        {name}
                    </div>

                    <div class="product-price">
                        ₹{price:,.2f}
                    </div>

                    <div class="product-stock">
                        {quantity} units available
                    </div>

                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "Add to Cart",
                    key=f"product_{product['id']}",
                    use_container_width=True,
                    disabled=quantity <= 0
                ):

                    product_id = product["id"]

                    if product_id in st.session_state.cart:

                        st.session_state.cart[
                            product_id
                        ]["quantity"] += 1

                    else:

                        st.session_state.cart[product_id] = {
                            "name": product["name"],
                            "price": price,
                            "quantity": 1
                        }

                    st.toast(f"{name} added to cart!")

except requests.exceptions.RequestException:

    st.error(
        "Unable to connect to the backend. "
        "Please start FastAPI."
    )


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px; color:#667085;">

    <h3 style="color:#101828;">CHAITU STORE.</h3>

    Your shopping experience, simplified.

    <p style="font-size:12px;">
        Built with Streamlit + FastAPI
    </p>

</div>
""", unsafe_allow_html=True)
