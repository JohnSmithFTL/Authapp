# Home.py
import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path

def make_hashed_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password(password, hashed_password):
    """Check hashed password against stored password."""
    return make_hashed_password(password) == hashed_password

def load_users():
    """Load users from Excel file, create if doesn't exist."""
    users_file = Path("users.xlsx")
    if users_file.exists():
        return pd.read_excel(users_file)
    else:
        # Create with admin user
        df = pd.DataFrame({
            'user_id': ['admin'],
            'username': ['Administrator'],
            'password': [make_hashed_password('admin123')],
            'is_admin': [True]
        })
        df.to_excel(users_file, index=False)
        return df

def save_users(df):
    """Save users DataFrame to Excel."""
    df.to_excel("users.xlsx", index=False)

def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

def main():
    init_session_state()
    
    # Create sidebar with logout button and user info if authenticated
    if st.session_state.authenticated:
        with st.sidebar:
            st.write(f"User ID: {st.session_state.user_id}")
            st.write(f"Name: {st.session_state.username}")
            if st.session_state.is_admin:
                st.write("Role: Administrator")
            else:
                st.write("Role: User")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.user_id = None
                st.session_state.is_admin = False
                st.rerun()
    
    # Show login page or main content based on authentication status
    if not st.session_state.authenticated:
        st.title("Login")
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:  # Sign In
            with st.form("login_form"):
                login_id = st.text_input("User ID")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In")
                
                if submit:
                    users_df = load_users()
                    user = users_df[users_df['user_id'] == login_id]
                    
                    if not user.empty and check_password(password, user.iloc[0]['password']):
                        st.session_state.authenticated = True
                        st.session_state.username = user.iloc[0]['username']
                        st.session_state.user_id = login_id
                        st.session_state.is_admin = bool(user.iloc[0].get('is_admin', False))
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid User ID or password")
        
        with tab2:  # Sign Up
            with st.form("signup_form"):
                st.subheader("Create New Account")
                new_user_id = st.text_input(
                    "Choose User ID",
                    help="4-15 characters, letters and numbers only"
                )
                new_username = st.text_input("Full Name")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Sign Up")
                
                if submit:
                    if len(new_user_id) < 4 or len(new_user_id) > 15:
                        st.error("User ID must be between 4 and 15 characters!")
                        return
                        
                    if len(new_username) < 3:
                        st.error("Name must be at least 3 characters long!")
                        return
                        
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                        return
                        
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                        return
                    
                    users_df = load_users()
                    
                    if new_user_id in users_df['user_id'].values:
                        st.error("This User ID is already taken! Please choose another.")
                        return
                    
                    new_user = pd.DataFrame({
                        'user_id': [new_user_id],
                        'username': [new_username],
                        'password': [make_hashed_password(new_password)],
                        'is_admin': [False]  # New users are not admins by default
                    })
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    save_users(users_df)
                    st.success("Account created successfully!")
                    st.info("Please sign in with your User ID and password.")
    else:
        st.title("Welcome to the Main App!")
        st.write(f"Welcome back, {st.session_state.username}!")
        # Your main app content here

if __name__ == "__main__":
    main()
