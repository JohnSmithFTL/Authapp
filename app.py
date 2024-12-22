import streamlit as st
import streamlit_authenticator as stauth

# User credentials for authentication
usernames = ["admin"]
passwords = ["admin123"]
names = ["Admin User"]
emails = ["admin@example.com"]

# Hash the passwords properly
hashed_passwords = stauth.Hasher(passwords).generate()

# Create the credentials dictionary
credentials = {
    "usernames": {
        usernames[i]: {
            "email": emails[i],
            "name": names[i],
            "password": hashed_passwords[i]
        }
        for i in range(len(usernames))
    }
}

# Create the authenticator object
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="user_cookie",
    cookie_key="random_key",
    cookie_expiry_days=1,
)

# Login page
def login_page():
    st.title("Login Page")

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.success(f"Welcome {name}!")
        app_navigation(username)
    elif authentication_status is False:
        st.error("Invalid username or password.")
    elif authentication_status is None:
        st.warning("Please enter your username and password.")

# App navigation after successful login
def app_navigation(username):
    st.sidebar.title(f"Hello, {username}!")
    st.sidebar.write("Choose an option:")
    
    option = st.sidebar.radio("Select a page", ["Home", "About", "Logout"])

    if option == "Home":
        st.write("Welcome to the Home page!")
    elif option == "About":
        st.write("This is a simple app with authentication.")
    elif option == "Logout":
        authenticator.logout("Logout", "sidebar")
        st.write("You have logged out.")

# Main function
def main():
    login_page()

if __name__ == "__main__":
    main()
