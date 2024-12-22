# app.py
import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path
import os

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def init_users_db():
    if not os.path.exists('users.xlsx'):
        df = pd.DataFrame(columns=['username', 'password'])
        # Add admin credentials
        admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
        df.loc[0] = ['admin', admin_pass]
        df.to_excel('users.xlsx', index=False)
    return pd.read_excel('users.xlsx')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users_df = pd.read_excel('users.xlsx')
    hashed_password = hash_password(password)
    user_exists = users_df[
        (users_df['username'] == username) & 
        (users_df['password'] == hashed_password)
    ].shape[0] > 0
    return user_exists

def signup(username, password):
    users_df = pd.read_excel('users.xlsx')
    if username in users_df['username'].values:
        return False, "Username already exists!"
    
    hashed_password = hash_password(password)
    new_user = pd.DataFrame({'username': [username], 'password': [hashed_password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_excel('users.xlsx', index=False)
    return True, "Signup successful! Please login."

def create_pages_folder():
    Path("pages").mkdir(exist_ok=True)

def main():
    st.title("Welcome to My App")
    
    # Initialize users database and pages folder
    init_users_db()
    create_pages_folder()

    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with tab2:
            st.subheader("Sign Up")
            new_username = st.text_input("Username", key="signup_username")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Sign Up"):
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    success, message = signup(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    else:
        st.success("You are logged in!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
