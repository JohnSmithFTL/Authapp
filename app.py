# File: app.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load configuration file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set page config
st.set_page_config(
    page_title="Multi-Page App",
    page_icon="🏠",
    layout="wide"
)

# Initialize authentication
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Create login widget
name, authentication_status, username = authenticator.login()  # Removed deprecated parameters

if authentication_status:
    # Show logout button in sidebar
    with st.sidebar:
        st.write(f'Welcome *{name}*')
        authenticator.logout('Logout')  # Removed deprecated parameter
        
        # Navigation
        st.sidebar.title('Navigation')
        selection = st.sidebar.radio("Go to", ["Home", "About", "Dashboard"])

    # Import and display selected page
    if selection == "Home":
        import pages.home
        pages.home.app()
    elif selection == "About":
        import pages.about
        pages.about.app()
    elif selection == "Dashboard":
        import pages.dashboard
        pages.dashboard.app(username)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
