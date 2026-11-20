
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


# Get the JWT token from Streamlit session state
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


# Place an order using the customer's cart
def checkout():

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    try:
        response = requests.post(
            f"{API_URL}/orders/checkout",
            headers=headers,
            timeout=15
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.json().get(
                "detail",
                "Checkout failed."
            )
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error)
        }


# Retrieve all orders belonging to the logged-in customer
def get_orders():

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    try:
        response = requests.get(
            f"{API_URL}/orders/",
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.json().get(
                "detail",
                "Unable to load orders."
            )
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error)
        }


# Retrieve details of one particular order
def get_order_by_id(order_id):

    headers = get_auth_headers()

    if not headers:
        return {
            "success": False,
            "error": "Please log in first."
        }

    try:
        response = requests.get(
            f"{API_URL}/orders/{order_id}",
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.json().get(
                "detail",
                "Unable to load order."
            )
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error)
        }
