# Import product API function
from services.api import get_products as api_get_products


# ==========================================
# GET ALL PRODUCTS
# ==========================================

def get_all_products():
    """
    Fetch all products from the FastAPI backend.
    """

    try:

        # Request products from FastAPI
        response = api_get_products()

        # Check whether API returned an error
        if isinstance(response, dict) and "error" in response:

            return {
                "success": False,
                "data": [],
                "error": response["error"]
            }

        # Validate API response
        if not isinstance(response, list):

            return {
                "success": False,
                "data": [],
                "error": "Invalid product response from server."
            }

        # Return successfully retrieved products
        return {
            "success": True,
            "data": response,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "data": [],
            "error": str(e)
        }


# ==========================================
# GET PRODUCT BY ID
# ==========================================

def get_product_by_id(product_id):
    """
    Retrieve a specific product using its ID.
    """

    response = get_all_products()

    # Handle API failure
    if not response["success"]:
        return None

    # Search for the requested product
    for product in response["data"]:

        if product["id"] == product_id:
            return product

    return None


# ==========================================
# SEARCH PRODUCTS
# ==========================================

def search_products(search_query):
    """
    Search products based on their names.
    """

    response = get_all_products()

    if not response["success"]:
        return []

    products = response["data"]

    # Return all products if search is empty
    if not search_query or not search_query.strip():
        return products

    # Normalize search query
    search_query = search_query.strip().lower()

    # Filter products by name
    filtered_products = [

        product for product in products

        if search_query in product["name"].lower()

    ]

    return filtered_products


# ==========================================
# FILTER PRODUCTS BY PRICE
# ==========================================

def filter_products(min_price=0, max_price=None):
    """
    Filter products based on their prices.
    """

    response = get_all_products()

    if not response["success"]:
        return []

    products = response["data"]

    # Filter products using price range
    filtered_products = [

        product for product in products

        if product["price"] >= min_price

        and (
            max_price is None
            or product["price"] <= max_price
        )

    ]

    return filtered_products