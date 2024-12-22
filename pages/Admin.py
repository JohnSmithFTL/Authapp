# pages/Admin.py
import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib

def check_admin():
    """Check if user is authenticated and is an admin."""
    if not st.session_state.authenticated:
        st.warning("Please login to access this page.")
        st.stop()
    if not st.session_state.is_admin:
        st.error("You don't have permission to access this page.")
        st.stop()

def make_hashed_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_users():
    """Load users from Excel file."""
    users_file = Path("users.xlsx")
    return pd.read_excel(users_file)

def save_users(df):
    """Save users DataFrame to Excel."""
    df.to_excel("users.xlsx", index=False)

def main():
    check_admin()
    
    st.title("Admin Panel")
    st.write(f"Welcome, Administrator {st.session_state.username}")
    
    # Load users data
    users_df = load_users()
    
    # User Management Section
    st.header("User Management")
    
    # Display user table
    st.subheader("Current Users")
    # Hide password column for display
    display_df = users_df.drop('password', axis=1)
    st.dataframe(display_df)
    
    # User Actions
    st.subheader("User Actions")
    
    # Delete User
    with st.expander("Delete User"):
        users_to_delete = st.multiselect(
            "Select users to delete",
            options=users_df[users_df['user_id'] != 'admin']['user_id'].tolist()
        )
        if st.button("Delete Selected Users"):
            if users_to_delete:
                users_df = users_df[~users_df['user_id'].isin(users_to_delete)]
                save_users(users_df)
                st.success(f"Deleted users: {', '.join(users_to_delete)}")
                st.rerun()
    
    # Reset Password
    with st.expander("Reset User Password"):
        user_to_reset = st.selectbox(
            "Select user to reset password",
            options=users_df['user_id'].tolist()
        )
        new_password = st.text_input("New Password", type="password")
        if st.button("Reset Password"):
            if new_password:
                users_df.loc[users_df['user_id'] == user_to_reset, 'password'] = make_hashed_password(new_password)
                save_users(users_df)
                st.success(f"Password reset for user: {user_to_reset}")
    
    # Make Admin
    with st.expander("Change Admin Status"):
        user_to_change = st.selectbox(
            "Select user",
            options=users_df[users_df['user_id'] != 'admin']['user_id'].tolist()
        )
        is_admin = st.checkbox("Is Admin")
        if st.button("Update Admin Status"):
            users_df.loc[users_df['user_id'] == user_to_change, 'is_admin'] = is_admin
            save_users(users_df)
            st.success(f"Updated admin status for user: {user_to_change}")
    
    # System Stats
    st.header("System Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(users_df))
    with col2:
        st.metric("Admin Users", len(users_df[users_df['is_admin'] == True]))
    with col3:
        st.metric("Regular Users", len(users_df[users_df['is_admin'] == False]))

if __name__ == "__main__":
    main()
