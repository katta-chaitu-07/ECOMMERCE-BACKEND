
import streamlit as st

from services.api import (
    register_user as api_register_user,
    login_user as api_login_user,
    get_current_user as api_get_current_user
)


# ==========================================
# USER REGISTRATION
# ==========================================

def register(name, email, password):
    """Register a new user through FastAPI."""

    return api_register_user(
        name=name,
        email=email,
        password=password
    )


# ==========================================
# USER LOGIN
# ==========================================

def login(email, password):
    """Authenticate user and store JWT token."""

    response = api_login_user(
        email=email,
        password=password
    )

    if not response.get("success"):
        return response

    data = response.get("data") or {}
    access_token = data.get("access_token")

    if not access_token:
        return {
            "success": False,
            "data": None,
            "error": "Access token was not received.",
            "status_code": response.get("status_code")
        }

    # Save JWT token
    st.session_state.access_token = access_token

    # Retrieve logged-in user details
    user_response = api_get_current_user(access_token)

    if not user_response.get("success"):

        st.session_state.access_token = None
        st.session_state.user = None
        st.session_state.authenticated = False

        return user_response

    # Save user information
    st.session_state.user = user_response.get("data")
    st.session_state.authenticated = True

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
    """Retrieve authenticated user's information."""

    access_token = st.session_state.get("access_token")

    if not access_token:
        return None

    response = api_get_current_user(access_token)

    if response.get("success"):

        st.session_state.user = response.get("data")
        st.session_state.authenticated = True

        return st.session_state.user

    # Clear invalid or expired token
    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.authenticated = False

    return None


# ==========================================
# CHECK AUTHENTICATION
# ==========================================

def is_authenticated():
    """Check whether a valid user session exists."""

    return (
        bool(st.session_state.get("access_token"))
        and st.session_state.get("user") is not None
    )


# ==========================================
# USER LOGOUT
# ==========================================

def logout():
    """Clear authentication and return to homepage."""

    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.authenticated = False

    st.session_state.page = "Home"

    st.rerun()
