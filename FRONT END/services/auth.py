
import streamlit as st

from services.api import (
    register_user as api_register_user,
    login_user as api_login_user,
    get_current_user as api_get_current_user
)


# ==========================================
# AUTHENTICATION SESSION HELPERS
# ==========================================

def get_access_token():
    """Get the JWT token from Streamlit session state."""

    return (
        st.session_state.get("access_token")
        or st.session_state.get("token")
    )


def clear_auth_session():
    """Clear all authentication-related session data."""

    st.session_state.access_token = None
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.authenticated = False


# ==========================================
# USER REGISTRATION
# ==========================================

def register(name, email, password):
    """Register a new user through FastAPI."""

    return api_register_user(
        name=name.strip(),
        email=email.strip(),
        password=password
    )


# ==========================================
# USER LOGIN
# ==========================================

def login(email, password):
    """Authenticate user and store JWT token."""

    # Remove any previous login before attempting a new one
    clear_auth_session()

    response = api_login_user(
        email=email.strip(),
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

    # Save the JWT token
    st.session_state.access_token = access_token
    st.session_state.token = access_token

    # Retrieve authenticated user details
    user_response = api_get_current_user(access_token)

    if not user_response.get("success"):

        clear_auth_session()

        return {
            "success": False,
            "data": None,
            "error": user_response.get(
                "error",
                "Unable to retrieve user details."
            ),
            "status_code": user_response.get("status_code")
        }

    # Save user information
    user = user_response.get("data")

    if not isinstance(user, dict):
        clear_auth_session()

        return {
            "success": False,
            "data": None,
            "error": "Invalid user information received.",
            "status_code": user_response.get("status_code")
        }

    st.session_state.user = user
    st.session_state.authenticated = True

    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "user": user
        },
        "error": None,
        "status_code": response.get("status_code")
    }


# ==========================================
# GET CURRENT USER
# ==========================================

def get_logged_in_user():
    """Retrieve authenticated user's information."""

    access_token = get_access_token()

    if not access_token:
        clear_auth_session()
        return None

    response = api_get_current_user(access_token)

    if response.get("success"):

        user = response.get("data")

        if isinstance(user, dict):
            st.session_state.access_token = access_token
            st.session_state.token = access_token
            st.session_state.user = user
            st.session_state.authenticated = True

            return user

    # Clear expired or invalid authentication
    clear_auth_session()

    return None


# ==========================================
# CHECK AUTHENTICATION
# ==========================================

def is_authenticated():
    """Check whether the user has an authenticated session."""

    return (
        bool(get_access_token())
        and st.session_state.get("authenticated", False)
        and st.session_state.get("user") is not None
    )


# ==========================================
# USER LOGOUT
# ==========================================

def logout():
    """Log out the user and return to homepage."""

    clear_auth_session()

    # Clear selected order and checkout confirmation
    st.session_state.pop("selected_order_id", None)
    st.session_state.pop("checkout_success_order", None)

    st.session_state.page = "Home"

    st.rerun()
