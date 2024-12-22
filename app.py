# File: app.py
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import bcrypt
import yaml
from yaml.loader import SafeLoader

# Load config.yaml
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Load users from Excel file
USERS_FILE = "users.xlsx"

def load_users():
    try:
        df = pd.read_excel(USERS_FILE)
        # Remove leading/trailing spaces from column names
        df.columns = df.columns.str.strip().str.lower()
        return df
    except FileNotFoundError:
        # Create new DataFrame if file doesn't exist
        df = pd.DataFrame(columns=['username', 'email', 'name', 'password'])
        df.to_excel(USERS_FILE, index=False)
        return df

def save_user(username, email, name, password):
    df = load_users()
    # Check if username already exists
    if username in df['username'].values:
        raise ValueError("Username already exists")
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = pd.DataFrame({
        'username': [username], 
        'email': [email], 
        'name': [name], 
        'password': [hashed_password]
    })
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USERS_FILE, index=False)

def setup_authentication():
    df = load_users()
    credentials = {
        "usernames": {
            row["username"]: {
                "email": row["email"],
                "name": row["name"],
                "password": row["password"]
            }
            for _, row in df.iterrows()
        }
    }
    return stauth.Authenticate(
        credentials,
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

def login_page():
    st.title("Login Page")
    
    authenticator = setup_authentication()
    
    name, authentication_status, username = authenticator.login("Login", "main")
    
    if authentication_status:
        st.success(f"Welcome {name}!")
        app_navigation(username, authenticator)
    elif authentication_status is False:
        st.error("Invalid username/password")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
        
        # Add sign up option below login
        if st.button("Don't have an account? Sign Up"):
            st.session_state['page'] = 'signup'
            sign_up_page()

def app_navigation(username, authenticator):
    with st.sidebar:
        authenticator.logout("Logout", "main")
        option = st.selectbox("Navigation", ["Home", "About", "Dashboard", "Sign Up"])
    
    if option == "Home":
        import pages.home
        pages.home.app(username)
    elif option == "About":
        import pages.about
        pages.about.app(username)
    elif option == "Dashboard":
        import pages.dashboard
        pages.dashboard.app(username)
    elif option == "Sign Up":
        sign_up_page()

def sign_up_page():
    st.title("Sign Up Page")
    st.write("Register as a new user")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Sign Up")
        
        if submit_button:
            if not username or not email or not name or not password:
                st.error("Please fill all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    save_user(username, email, name, password)
                    st.success("User registered successfully! Please log in.")
                    st.session_state['page'] = 'login'
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error saving user: {e}")

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'signup':
        sign_up_page()

if __name__ == "__main__":
    main()
