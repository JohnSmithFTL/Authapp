# pages/Dashboard.py
import streamlit as st
from utils import require_auth

@require_auth()
def main():
    # Page header
    st.title("Dashboard")
    st.write(f"Welcome {st.session_state.username}!")
    st.write(f"User ID: {st.session_state.user_id}")
    
    # Simple dashboard content
    st.header("Dashboard Overview")
    
    # Some sample metrics
    st.write("### Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("Total Sales")
        st.write("$10,000")
    
    with col2:
        st.write("Total Orders")
        st.write("150")
    
    with col3:
        st.write("Active Users")
        st.write("50")
    
    # Additional information
    st.write("### Recent Activity")
    st.write("- Last login: Today")
    st.write("- Last order: Yesterday")
    st.write("- System status: Active")

if __name__ == "__main__":
    main()

# pages/About.py
import streamlit as st
from utils import require_auth

@require_auth()
def main():
    # Page header
    st.title("About")
    st.write(f"Welcome {st.session_state.username}!")
    
    # About content
    st.header("About Our Company")
    st.write("""
    Welcome to our company dashboard system. This is a simple 
    demonstration of a secure web application built with Streamlit.
    """)
    
    # Company info
    st.write("### Company Information")
    st.write("- Founded: 2024")
    st.write("- Location: New York")
    st.write("- Industry: Technology")
    
    # Contact info
    st.write("### Contact Us")
    st.write("Email: contact@company.com")
    st.write("Phone: (555) 123-4567")
    st.write("Address: 123 Business Street, NY")

if __name__ == "__main__":
    main()
