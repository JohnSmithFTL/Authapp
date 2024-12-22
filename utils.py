# utils.py
import streamlit as st
import pandas as pd
import hashlib
import re
from config import *

def make_hashed_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password(password, hashed_password):
    """Check hashed password against stored password."""
    return make_hashed_password(password) == hashed_password

def is_valid_user_id(user_id):
    """Validate user ID format."""
    pattern = re.compile(f'^[a-zA-Z0-9]{{{USERID_MIN_LENGTH},{USERID_MAX_LENGTH}}}$')
    return bool(pattern.match(user_id))

def load_users():
    """Load users from Excel file, create if doesn't exist."""
    if not DATABASE_FILE.exists():
        df = pd.DataFrame(columns=['user_id', 'username', 'password'])
        df.to_excel(DATABASE_FILE, index=False)
        return df
    return pd.read_excel(DATABASE_FILE)

def save_users(df):
    """Save users DataFrame to Excel."""
    df.to_excel(DATABASE_FILE, index=False)

def init_session_state():
    """Initialize session state variables."""
    if SESSION_AUTH_KEY not in st.session_state:
        st.session_state[SESSION_AUTH_KEY] = False
    if SESSION_USERNAME_KEY not in st.session_state:
        st.session_state[SESSION_USERNAME_KEY] = None
    if SESSION_USERID_KEY not in st.session_state:
        st.session_state[SESSION_USERID_KEY] = None

def require_auth():
    """Decorator to require authentication for pages."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            init_session_state()
            if not st.session_state[SESSION_AUTH_KEY]:
                st.warning("Please login to access this page.")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator
