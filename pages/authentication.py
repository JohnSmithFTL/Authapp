# pages/authentication.py
import streamlit as st
from utils import (
    make_hashed_password, 
    load_users, 
    save_users, 
    is_valid_user_id,
    init_session_state
)
from config import *

def login_user(user_id, password):
    """Handle user login."""
    users_df = load_users()
    user = users_df[users_df['user_id'] == user_id]
    
    if not user.empty and check_password(password, user.iloc[0]['password']):
        st.session_state[SESSION_AUTH_KEY] = True
        st.session_state[SESSION_USERNAME_KEY] = user.iloc[0]['username']
        st.session_state[SESSION_USERID_KEY] = user_id
        return True
    return False

def register_user(user_id, username, password):
    """Handle user registration."""
    if not is_valid_user_id(user_id):
        raise ValueError("Invalid User ID format!")
        
    if len(username) < USERNAME_MIN_LENGTH:
        raise ValueError(f"Name must be at least {USERNAME_MIN_LENGTH} characters!")
        
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters!")
    
    users_df = load_users()
    if user_id in users_df['user_id'].values:
        raise ValueError("This User ID is already taken!")
    
    new_user = pd.DataFrame({
        'user_id': [user_id],
        'username': [username],
        'password': [make_hashed_password(password)]
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
