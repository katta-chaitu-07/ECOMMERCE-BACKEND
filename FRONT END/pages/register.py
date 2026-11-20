
# ============================================
# CHAITU STORE - USER REGISTRATION PAGE
# ============================================

import streamlit as st

from services.auth import register, is_authenticated


def render_register_page():

    st.title("📝 Create Your Account")
    st.caption("Join Chaitu Store and start shopping!")

    # Already authenticated users don't need to register again
    if is_authenticated():

        st.success("You are already logged in!")

        if st.button("Continue Shopping", use_container_width=True):
            st.session_state.page = "Products"
            st.rerun()

        return

    # Registration form
    with st.form("registration_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            placeholder="Create a password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            placeholder="Re-enter your password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True,
            type="primary"
        )

    if submitted:

        # ------------------------------------
        # Input Validation
        # ------------------------------------

        if not name.strip() or not email.strip() or not password:
            st.warning("Please fill in all the fields.")

        elif "@" not in email or "." not in email.split("@")[-1]:
            st.warning("Please enter a valid email address.")

        elif len(password) < 8:
            st.warning("Password must contain at least 8 characters.")

        elif password != confirm_password:
            st.warning("Passwords do not match.")

        else:

            # --------------------------------
            # Call FastAPI Registration
            # --------------------------------

            with st.spinner("Creating your account..."):

                response = register(
                    name=name.strip(),
                    email=email.strip(),
                    password=password
                )

            if response.get("success"):

                st.success("🎉 Account created successfully!")

                st.session_state.registration_success = True

                st.info("You can now log in using your registered email.")

                if st.button("Go to Login", use_container_width=True):
                    st.session_state.registration_success = False
                    st.session_state.page = "Login"
                    st.rerun()

            else:

                st.error(
                    response.get(
                        "error",
                        "Registration failed. Please try again."
                    )
                )

    st.divider()

    st.write("Already have an account?")

    if st.button("Login Instead", use_container_width=True):
        st.session_state.page = "Login"
        st.rerun()
