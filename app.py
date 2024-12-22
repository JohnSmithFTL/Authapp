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
    df = pd.read_excel(USERS_FILE)
    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()
    # Debugging line to inspect the DataFrame structure and column names
    st.write("Loaded columns:", df.columns)  # Display column names
    st.write(df.head())  # Display first few rows of the DataFrame
    return df

def save_user(username, email, name, password):
    df = load_users()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = pd.DataFrame({'username': [username], 'email': [email], 'name': [name], 'password': [hashed_password]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USERS_FILE, index=False)

# Authentication Setup
df = load_users()

# Verify the column names in the loaded DataFrame
expected_columns = ["username", "email", "name", "password"]
if not all(col in df.columns for col in expected_columns):
    st.error(f"Expected columns {expected_columns} not found in the users file. Please check the column names.")
else:
    credentials = {
        "usernames": {row["username"]: {"email": row["email"], "name": row["name"], "password": row["password"]}
                    for _, row in df.iterrows()}
    }
    authenticator = stauth.Authenticate(
        credentials,
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

# Login Page
def login_page():
    st.title("Login Page")
    
    # Simplified login without location argument
    login_result = authenticator.login("Login")  # Removed location="main"
    
    # Debugging: Print the entire login result to inspect its structure
    st.write("Login result:", login_result)
    
    if login_result is not None:
        try:
            name, authentication_status, username = login_result
            if authentication_status:
                st.success(f"Welcome {name}!")
                app_navigation(username)
            elif authentication_status is False:
                st.error("Invalid username/password")
            elif authentication_status is None:
                st.warning("Please enter your username and password")
        except Exception as e:
            st.error(f"Error unpacking login result: {e}")
    else:
        st.error("Authentication result is None")

# App Navigation
def app_navigation(username):
    option = st.sidebar.selectbox("Navigation", ["Home", "About", "Dashboard", "Sign Up", "Logout"])
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
    elif option == "Logout":
        authenticator.logout("Logout", "sidebar")

# Sign Up Page
def sign_up_page():
    st.title("Sign Up Page")
    st.write("Register as a new user")
    
    username = st.text_input("Username")
    email = st.text_input("Email")
    name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if not username or not email or not name or not password:
            st.error("Please fill all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # Save user to Excel
            try:
                save_user(username, email, name, password)
                st.success("User registered successfully! Please log in.")
            except Exception as e:
                st.error(f"Error saving user: {e}")

# Main Function
def main():
    login_page()

if __name__ == "__main__":
    main()
