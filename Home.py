# Home.py
import streamlit as st
from utils import init_session_state
from pages.authentication import login_user, register_user

def main():
    init_session_state()
    
    # Sidebar user info and logout
    if st.session_state[SESSION_AUTH_KEY]:
        with st.sidebar:
            st.write(f"User ID: {st.session_state[SESSION_USERID_KEY]}")
            st.write(f"Name: {st.session_state[SESSION_USERNAME_KEY]}")
            if st.button("Logout"):
                for key in [SESSION_AUTH_KEY, SESSION_USERNAME_KEY, SESSION_USERID_KEY]:
                    st.session_state[key] = None
                st.rerun()
    
    # Main content
    if not st.session_state[SESSION_AUTH_KEY]:
        st.title("Login")
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:  # Sign In
            with st.form("login_form"):
                user_id = st.text_input("User ID")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In")
                
                if submit:
                    try:
                        if login_user(user_id, password):
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid User ID or password")
                    except Exception as e:
                        st.error(f"Login error: {str(e)}")
        
        with tab2:  # Sign Up
            with st.form("signup_form"):
                new_user_id = st.text_input(
                    "Choose User ID",
                    help=f"{USERID_MIN_LENGTH}-{USERID_MAX_LENGTH} characters, letters and numbers only"
                )
                new_username = st.text_input("Full Name")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Sign Up")
                
                if submit:
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                    else:
                        try:
                            register_user(new_user_id, new_username, new_password)
                            st.success("Account created successfully!")
                            st.info("Please sign in with your new account.")
                        except ValueError as e:
                            st.error(str(e))
    else:
        st.title("Welcome to the Main App!")
        st.write(f"Welcome back, {st.session_state[SESSION_USERNAME_KEY]}!")
        # Your main app content here

if __name__ == "__main__":
    main()

# pages/Dashboard.py
import streamlit as st
from utils import require_auth

@require_auth()
def main():
    st.title("Dashboard")
    st.write(f"Welcome {st.session_state[SESSION_USERNAME_KEY]}!")
    st.write(f"Your User ID: {st.session_state[SESSION_USERID_KEY]}")
    
    # Your dashboard content here
    st.header("Dashboard Content")
    # Add your dashboard components here

if __name__ == "__main__":
    main()

# pages/About.py
import streamlit as st
from utils import require_auth

@require_auth()
def main():
    st.title("About")
    st.write(f"Welcome {st.session_state[SESSION_USERNAME_KEY]}!")
    
    # Your about page content here
    st.header("About Content")
    # Add your about page content here

if __name__ == "__main__":
    main()
