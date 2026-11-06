# ============================================
# CHAITU STORE - API SERVICE
# Handles frontend-backend communication
# ============================================

import requests

from config import (
    PRODUCTS_URL,
    REGISTER_URL,
    LOGIN_URL,
    PROFILE_URL
)


# ============================================
# 1. COMMON API SETTINGS
# ============================================

TIMEOUT = 10


# ============================================
# 2. GET ALL PRODUCTS
# ============================================

def get_products():

    try:
        response = requests.get(
            PRODUCTS_URL,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        return {
            "error": f"Unable to fetch products: {error}"
        }


# ============================================
# 3. USER REGISTRATION
# ============================================

def register_user(name, email, password):

    data = {
        "name": name,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(
            REGISTER_URL,
            json=data,
            timeout=TIMEOUT
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================
# 4. USER LOGIN
# ============================================

def login_user(email, password):

    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(
            LOGIN_URL,
            json=data,
            timeout=TIMEOUT
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================
# 5. GET LOGGED-IN USER PROFILE
# ============================================

def get_current_user(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(
            PROFILE_URL,
            headers=headers,
            timeout=TIMEOUT
        )

        if response.ok:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }