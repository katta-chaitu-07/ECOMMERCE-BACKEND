
from services.api import get_products as api_get_products


# ==========================================
# GET ALL PRODUCTS
# ==========================================

def get_all_products():
    """Fetch and validate products from FastAPI."""

    try:
        response = api_get_products()

        if isinstance(response, dict):

            if not response.get("success", False):
                return {
                    "success": False,
                    "data": [],
                    "error": response.get("error")
                    or "Unable to fetch products."
                }

            products = response.get("data")

        elif isinstance(response, list):
            products = response

        else:
            return {
                "success": False,
                "data": [],
                "error": "Unexpected response from product API."
            }

        if not isinstance(products, list):
            return {
                "success": False,
                "data": [],
                "error": "Product data is not a valid list."
            }

        valid_products = []

        for product in products:

            if not isinstance(product, dict):
                continue

            if not all(
                key in product
                for key in ("id", "name", "price", "quantity")
            ):
                continue

            try:
                image_url = product.get("image_url")

                clean_product = {
                    "id": int(product["id"]),
                    "name": str(product["name"]),
                    "price": float(product["price"]),
                    "quantity": int(product["quantity"]),
                    "image_url": (
                        str(image_url).strip()
                        if image_url and str(image_url).strip()
                        else None
                    )
                }

                valid_products.append(clean_product)

            except (TypeError, ValueError):
                continue

        return {
            "success": True,
            "data": valid_products,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "data": [],
            "error": str(error)
        }


# ==========================================
# GET PRODUCT BY ID
# ==========================================

def get_product_by_id(product_id):

    response = get_all_products()

    if not response["success"]:
        return None

    for product in response["data"]:
        if product["id"] == product_id:
            return product

    return None


# ==========================================
# SEARCH PRODUCTS
# ==========================================

def search_products(search_query):

    response = get_all_products()

    if not response["success"]:
        return []

    products = response["data"]

    if not search_query or not search_query.strip():
        return products

    search_query = search_query.strip().lower()

    return [
        product for product in products
        if search_query in product["name"].lower()
    ]


# ==========================================
# FILTER PRODUCTS BY PRICE
# ==========================================

def filter_products(min_price=0, max_price=None):

    response = get_all_products()

    if not response["success"]:
        return []

    try:
        min_price = float(min_price)

        if max_price is not None:
            max_price = float(max_price)

    except (TypeError, ValueError):
        return []

    if min_price < 0:
        return []

    if max_price is not None and max_price < min_price:
        return []

    return [
        product for product in response["data"]
        if product["price"] >= min_price
        and (
            max_price is None
            or product["price"] <= max_price
        )
    ]
