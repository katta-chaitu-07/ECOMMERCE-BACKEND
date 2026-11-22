import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Read the deployed backend URL from Streamlit Secrets
try:
    BASE_URL = st.secrets["API_BASE_URL"].rstrip("/")
except (KeyError, FileNotFoundError):
    BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:8000"
    ).rstrip("/")

# API endpoints
PRODUCTS_URL = f"{BASE_URL}/products/"
REGISTER_URL = f"{BASE_URL}/users/register"
LOGIN_URL = f"{BASE_URL}/users/login"
PROFILE_URL = f"{BASE_URL}/users/me"

# Store information
STORE_NAME = "CHAITU STORE"
STORE_TAGLINE = "Discover Products. Enjoy Shopping."
CURRENCY = "₹"