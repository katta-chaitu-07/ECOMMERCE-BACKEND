
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


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


def add_to_cart(product_id, quantity=1):

    headers = get_auth_headers()

    if not headers:
        return {"success": False, "error": "Please log in first."}

    try:
        response = requests.post(
            f"{API_URL}/cart/add/{product_id}",
            params={"quantity": quantity},
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {"success": True, "data": response.json()}

        return {
            "success": False,
            "error": response.json().get("detail", "Unable to add product.")
        }

    except requests.RequestException as error:
        return {"success": False, "error": str(error)}


def get_cart():

    headers = get_auth_headers()

    if not headers:
        return {"success": False, "error": "Please log in first."}

    try:
        response = requests.get(
            f"{API_URL}/cart/",
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {"success": True, "data": response.json()}

        return {
            "success": False,
            "error": response.json().get("detail", "Unable to load cart.")
        }

    except requests.RequestException as error:
        return {"success": False, "error": str(error)}


def update_cart_item(product_id, quantity):

    headers = get_auth_headers()

    if not headers:
        return {"success": False, "error": "Please log in first."}

    try:
        response = requests.put(
            f"{API_URL}/cart/update/{product_id}",
            params={"quantity": quantity},
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {"success": True, "data": response.json()}

        return {
            "success": False,
            "error": response.json().get("detail", "Unable to update cart.")
        }

    except requests.RequestException as error:
        return {"success": False, "error": str(error)}


def remove_from_cart(product_id):

    headers = get_auth_headers()

    if not headers:
        return {"success": False, "error": "Please log in first."}

    try:
        response = requests.delete(
            f"{API_URL}/cart/remove/{product_id}",
            headers=headers,
            timeout=10
        )

        if response.ok:
            return {"success": True, "data": response.json()}

        return {
            "success": False,
            "error": response.json().get("detail", "Unable to remove product.")
        }

    except requests.RequestException as error:
        return {"success": False, "error": str(error)}
