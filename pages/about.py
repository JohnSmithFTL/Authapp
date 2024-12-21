# File: pages/about.py
import streamlit as st

def app():
    st.title('ℹ️ About')
    
    st.write("""
    ## About Our Platform
    This is a sophisticated multi-page application built with Streamlit.
    """)
    
    # Company info
    with st.expander("Company Information"):
        st.write("""
        ### Our Mission
        To provide the best user experience through innovative solutions.
        
        ### Our Vision
        Building the future of web applications.
        """)
    
    # Features
    st.subheader("Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        #### Security
        - Secure authentication
        - Role-based access
        - Data encryption
        """)
        
    with col2:
        st.write("""
        #### Analytics
        - Real-time data
        - Interactive dashboards
        - Custom reports
        """)
    
    # Contact form
    st.subheader("Contact Us")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Message")
        
        if submit:
            st.success("Thank you for your message! We'll get back to you soon.")
