
import requests

API_URL = "http://127.0.0.1:8000"

TIMEOUT = 10


def make_request(method, endpoint, data=None, token=None):

    url = f"{API_URL}{endpoint}"

    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:

        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=headers,
            timeout=TIMEOUT
        )

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        if response.ok:

            return {
                "success": True,
                "data": response_data,
                "error": None,
                "status_code": response.status_code
            }

        detail = response_data.get(
            "detail",
            "Something went wrong."
        )

        return {
            "success": False,
            "data": None,
            "error": detail,
            "status_code": response.status_code
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "data": None,
            "error": "Cannot connect to backend. Start FastAPI first.",
            "status_code": None
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "data": None,
            "error": "Request timed out. Please try again.",
            "status_code": None
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "data": None,
            "error": str(error),
            "status_code": None
        }


# ==========================================
# USER REGISTRATION
# ==========================================

def register_user(name, email, password):

    return make_request(
        method="POST",
        endpoint="/users/register",
        data={
            "name": name,
            "email": email,
            "password": password
        }
    )


# ==========================================
# USER LOGIN
# ==========================================

def login_user(email, password):

    return make_request(
        method="POST",
        endpoint="/users/login",
        data={
            "email": email,
            "password": password
        }
    )


# ==========================================
# GET LOGGED-IN USER
# ==========================================

def get_current_user(token):

    return make_request(
        method="GET",
        endpoint="/users/me",
        token=token
    )


# ==========================================
# GET ALL PRODUCTS
# ==========================================

def get_products():

    return make_request(
        method="GET",
        endpoint="/products/"
    )
