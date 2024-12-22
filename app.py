# app.py with improved signup and database handling
import streamlit as st
import pandas as pd
import hashlib
import os

def init_users_db():
    """Initialize the users database if it doesn't exist"""
    if not os.path.exists('users.xlsx'):
        df = pd.DataFrame(columns=['username', 'password'])
        # Add admin credentials
        admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
        df.loc[0] = ['admin', admin_pass]
        df.to_excel('users.xlsx', index=False)
        print("Created new users database with admin account")
    return pd.read_excel('users.xlsx')

def signup(username, password):
    """Enhanced signup function with proper error handling and verification"""
    try:
        # Read existing users
        if os.path.exists('users.xlsx'):
            users_df = pd.read_excel('users.xlsx')
        else:
            users_df = pd.DataFrame(columns=['username', 'password'])
        
        # Check if username already exists
        if username in users_df['username'].values:
            return False, "Username already exists!"
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create new user entry
        new_user = pd.DataFrame({
            'username': [username],
            'password': [hashed_password]
        })
        
        # Append new user to existing database
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        
        # Save the updated database
        users_df.to_excel('users.xlsx', index=False)
        
        # Verify the save was successful
        verification_df = pd.read_excel('users.xlsx')
        if username in verification_df['username'].values:
            print(f"Successfully added user: {username}")
            return True, "Signup successful! Please login."
        else:
            return False, "Error saving user data. Please try again."
            
    except Exception as e:
        print(f"Error during signup: {str(e)}")
        return False, f"An error occurred: {str(e)}"

def verify_database():
    """Function to verify database contents"""
    try:
        if os.path.exists('users.xlsx'):
            df = pd.read_excel('users.xlsx')
            print("\nCurrent Database Contents:")
            print("Usernames:", df['username'].tolist())
            print("Total users:", len(df))
            return True
        else:
            print("Database file not found!")
            return False
    except Exception as e:
        print(f"Error verifying database: {str(e)}")
        return False

# Modified main function with debug information
def main():
    st.title("Welcome to My App")
    
    # Initialize users database
    init_users_db()
    
    if not st.session_state.get('authenticated', False):
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
                if not new_username or not new_password:
                    st.error("Username and password are required!")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    success, message = signup(new_username, new_password)
                    if success:
                        st.success(message)
                        # Verify the database after signup
                        if verify_database():
                            st.info("User database updated successfully!")
                    else:
                        st.error(message)
    
    else:
        st.success("You are logged in!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

# Add this at the end of your script to verify database on startup
if __name__ == "__main__":
    print("Initializing application...")
    verify_database()
    main()
