import streamlit as st


def admin_login():
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if st.session_state.admin_authenticated:
        return True

    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if (
            username == st.secrets["ADMIN_USERNAME"]
            and password == st.secrets["ADMIN_PASSWORD"]
        ):
            st.session_state.admin_authenticated = True
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

    return False


def admin_logout():
    st.session_state.admin_authenticated = False
    st.success("🔓 Logged out")
    st.rerun()
