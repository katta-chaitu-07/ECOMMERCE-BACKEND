
# ============================================
# CHAITU STORE - CART API SERVICE
# ============================================

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
TIMEOUT = 10


# ============================================
# AUTHENTICATION HEADERS
# ============================================

def get_auth_headers():

    token = (
        st.session_state.get("access_token")
        or st.session_state.get("token")
    )

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================
# COMMON RESPONSE HANDLER
# ============================================

def handle_response(response, default_error):

    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.ok:
        return {
            "success": True,
            "data": data,
            "error": None,
            "status_code": response.status_code
        }

    if isinstance(data, dict):
        error = data.get("detail", default_error)
    else:
        error = default_error

    return {
        "success": False,
        "data": None,
        "error": error,
        "status_code": response.status_code
    }


# ============================================
# ADD PRODUCT TO CART
# ============================================

def add_to_cart(product_id, quantity=1):

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    if not isinstance(product_id, int) or product_id <= 0:
        return {
            "success": False,
            "error": "Invalid product ID."
        }

    if not isinstance(quantity, int) or quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be a positive integer."
        }

    try:

        response = requests.post(
            f"{API_URL}/cart/add/{product_id}",
            params={"quantity": quantity},
            headers=headers,
            timeout=TIMEOUT
        )

        return handle_response(
            response,
            "Unable to add product to cart."
        )

    except requests.Timeout:

        return {
            "success": False,
            "error": "Request timed out. Please try again."
        }

    except requests.ConnectionError:

        return {
            "success": False,
            "error": "Cannot connect to the server. Check your backend."
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================
# GET SHOPPING CART
# ============================================

def get_cart():

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    try:

        response = requests.get(
            f"{API_URL}/cart/",
            headers=headers,
            timeout=TIMEOUT
        )

        return handle_response(
            response,
            "Unable to load your cart."
        )

    except requests.Timeout:

        return {
            "success": False,
            "error": "Request timed out while loading cart."
        }

    except requests.ConnectionError:

        return {
            "success": False,
            "error": "Cannot connect to the backend server."
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================
# UPDATE CART ITEM QUANTITY
# ============================================

def update_cart_item(product_id, quantity):

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    if not isinstance(product_id, int) or product_id <= 0:
        return {
            "success": False,
            "error": "Invalid product ID."
        }

    if not isinstance(quantity, int) or quantity <= 0:
        return {
            "success": False,
            "error": "Quantity must be greater than zero."
        }

    try:

        response = requests.put(
            f"{API_URL}/cart/update/{product_id}",
            params={"quantity": quantity},
            headers=headers,
            timeout=TIMEOUT
        )

        return handle_response(
            response,
            "Unable to update cart item."
        )

    except requests.Timeout:

        return {
            "success": False,
            "error": "Request timed out while updating cart."
        }

    except requests.ConnectionError:

        return {
            "success": False,
            "error": "Cannot connect to the backend server."
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================
# REMOVE PRODUCT FROM CART
# ============================================

def remove_from_cart(product_id):

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    if not isinstance(product_id, int) or product_id <= 0:
        return {
            "success": False,
            "error": "Invalid product ID."
        }

    try:

        response = requests.delete(
            f"{API_URL}/cart/remove/{product_id}",
            headers=headers,
            timeout=TIMEOUT
        )

        return handle_response(
            response,
            "Unable to remove product from cart."
        )

    except requests.Timeout:

        return {
            "success": False,
            "error": "Request timed out while removing product."
        }

    except requests.ConnectionError:

        return {
            "success": False,
            "error": "Cannot connect to the backend server."
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }
