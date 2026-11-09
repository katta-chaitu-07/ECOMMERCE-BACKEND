import streamlit as st

# Import registration service
from services.auth import register


# ==========================================
# REGISTRATION PAGE
# ==========================================

def render_register_page():

    # Page heading
    st.title("👤 Create Your Account")

    st.write("Join Chaitu Store and start shopping.")

    st.markdown("---")

    # Registration form
    with st.form("register_form"):

        # Full name
        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        # Email address
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        # Password
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        # Confirm password
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        # Submit button
        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        # ======================================
        # REGISTRATION VALIDATION
        # ======================================

        if submitted:

            # Check empty fields
            if not name.strip() or not email.strip() or not password:

                st.error("Please fill in all required fields.")

            # Basic email validation
            elif (
                "@" not in email
                or "." not in email.split("@")[-1]
            ):

                st.error("Please enter a valid email address.")

            # Check password confirmation
            elif password != confirm_password:

                st.error("Passwords do not match.")

            # Check password length
            elif len(password) < 8:

                st.error(
                    "Password must contain at least 8 characters."
                )

            else:

                # Connect to FastAPI registration endpoint
                with st.spinner("Creating your account..."):

                    response = register(
                        name=name.strip(),
                        email=email.strip(),
                        password=password
                    )

                # Check backend response
                if response.get("success"):

                    st.success(
                        "Registration successful! Your account has been created."
                    )

                    # Store registration status
                    st.session_state.registration_success = True

                else:

                    st.error(
                        response.get("error", "Registration failed.")
                    )

    # ======================================
    # LOGIN NAVIGATION
    # ======================================

    if st.session_state.get("registration_success", False):

        if st.button("Continue to Login"):

            st.session_state.registration_success = False

            st.session_state.page = "Login"

            st.rerun()

    else:

        if st.button("Already have an account? Login"):

            st.session_state.page = "Login"

            st.rerun()