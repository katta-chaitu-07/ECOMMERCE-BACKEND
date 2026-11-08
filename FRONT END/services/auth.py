import streamlit as st

# Import authentication API functions from api.py
from services.api import (
    register_user as api_register_user,
    login_user as api_login_user,
    get_current_user as api_get_current_user
)


# ==========================================
# USER REGISTRATION
# ==========================================

def register(name, email, password):
    """
    Register a new user through the FastAPI backend.
    """

    response = api_register_user(
        name=name,
        email=email,
        password=password
    )

    return response


# ==========================================
# USER LOGIN
# ==========================================

def login(email, password):
    """
    Authenticate the user and store the JWT token.
    """

    # Send login credentials to FastAPI
    response = api_login_user(
        email=email,
        password=password
    )

    # Check whether login was successful
    if not response.get("success"):
        return response

    # Extract login response data
    data = response.get("data") or {}

    # Extract JWT access token
    access_token = data.get("access_token")

    # Verify that backend returned a token
    if not access_token:
        return {
            "success": False,
            "data": None,
            "error": "Access token was not received.",
            "status_code": response.get("status_code")
        }

    # Store JWT token in Streamlit session
    st.session_state.access_token = access_token

    # Fetch authenticated user's information
    user_response = api_get_current_user(access_token)

    # Check whether user information was retrieved
    if not user_response.get("success"):

        st.session_state.access_token = None
        st.session_state.user = None

        return user_response

    # Store user information in session
    st.session_state.user = user_response.get("data")

    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "user": st.session_state.user
        },
        "error": None,
        "status_code": response.get("status_code")
    }


# ==========================================
# GET CURRENT USER
# ==========================================

def get_logged_in_user():
    """
    Retrieve the currently authenticated user's information.
    """

    # Get JWT token from session
    access_token = st.session_state.get("access_token")

    if not access_token:
        return None

    # Request user information from FastAPI
    response = api_get_current_user(access_token)

    if response.get("success"):

        st.session_state.user = response.get("data")

        return st.session_state.user

    # Clear invalid or expired authentication
    st.session_state.access_token = None
    st.session_state.user = None

    return None


# ==========================================
# CHECK AUTHENTICATION STATUS
# ==========================================

def is_authenticated():
    """
    Check whether a user is currently logged in.
    """

    return (
        st.session_state.get("access_token") is not None
        and st.session_state.get("user") is not None
    )


# ==========================================
# USER LOGOUT
# ==========================================

def logout():
    """
    Log out the user and clear authentication data.
    """

    # Remove JWT token
    st.session_state.access_token = None

    # Remove user information
    st.session_state.user = None

    # Navigate back to homepage
    st.session_state.page = "Home"

    # Refresh Streamlit application
    st.rerun()