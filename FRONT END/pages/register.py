
import streamlit as st

from services.auth import register


def render_register_page():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("📝 Create Your Account")

    st.caption(
        "Join Chaitu Store and start your shopping journey."
    )

    st.divider()

    # ==========================================
    # REGISTRATION FORM
    # ==========================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        with st.container(border=True):

            st.subheader("Create a New Account")

            with st.form("registration_form"):

                name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

                email = st.text_input(
                    "Email Address",
                    placeholder="example@gmail.com"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                submitted = st.form_submit_button(
                    "Create Account",
                    type="primary",
                    use_container_width=True
                )

                if submitted:

                    # Validate input fields

                    if not name.strip() or not email.strip() or not password:
                        st.warning("Please fill in all fields.")

                    elif "@" not in email or "." not in email:
                        st.warning("Please enter a valid email address.")

                    elif len(password) < 8:
                        st.warning(
                            "Password must contain at least 8 characters."
                        )

                    elif password != confirm_password:
                        st.error("Passwords do not match.")

                    else:

                        # Send registration details to backend

                        response = register(
                            name=name.strip(),
                            email=email.strip(),
                            password=password
                        )

                        if response.get("success"):

                            st.success(
                                "Account created successfully!"
                            )

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

            if st.button(
                "Login Instead",
                use_container_width=True
            ):

                st.session_state.page = "Login"
                st.rerun()

    # ==========================================
    # FOOTER
    # ==========================================

    st.divider()

    st.caption(
        "Chaitu Store | Your Style. Your Choice. Your Store."
    )
