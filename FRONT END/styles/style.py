# ============================================
# CHAITU STORE - GLOBAL WEBSITE STYLING
# ============================================

import streamlit as st


def load_css():

    st.markdown("""

    <style>

    /* =====================================
       1. GLOBAL WEBSITE STYLING
    ===================================== */

    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }

    /* Main content container */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* =====================================
       2. HEADINGS
    ===================================== */

    h1, h2, h3, h4 {
        color: #0F172A;
        font-weight: 700;
    }

    h1 {
        font-size: 2.5rem;
    }

    h2 {
        font-size: 2rem;
    }


    /* =====================================
       3. BUTTONS
    ===================================== */

    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
        border: none;
        transform: translateY(-2px);
    }


    /* =====================================
       4. INPUT FIELDS
    ===================================== */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        background-color: white;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 1px #2563EB;
    }


    /* =====================================
       5. PRODUCT CARD
    ===================================== */

    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
        transition: all 0.3s ease;
    }

    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.10);
    }


    /* =====================================
       6. HERO SECTION
    ===================================== */

    .hero-section {
        background: linear-gradient(
            120deg,
            #0F172A,
            #1D4ED8
        );

        padding: 55px 40px;
        border-radius: 18px;
        color: white;
        margin-bottom: 35px;
    }

    .hero-section h1 {
        color: white;
        font-size: 2.8rem;
    }

    .hero-section p {
        color: #DBEAFE;
        font-size: 1.1rem;
    }


    /* =====================================
       7. SECTION TITLES
    ===================================== */

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 25px;
        margin-bottom: 20px;
    }


    /* =====================================
       8. DIVIDERS
    ===================================== */

    hr {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin-top: 25px;
        margin-bottom: 25px;
    }


    /* =====================================
       9. FOOTER
    ===================================== */

    .footer {
        background-color: #0F172A;
        color: #CBD5E1;
        padding: 25px;
        text-align: center;
        border-radius: 12px;
        margin-top: 50px;
    }

    .footer p {
        margin: 5px;
    }


    /* =====================================
       10. HIDE STREAMLIT BRANDING
    ===================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>

    """, unsafe_allow_html=True)