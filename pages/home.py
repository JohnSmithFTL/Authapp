# File: pages/home.py
import streamlit as st

def app():
    st.title('🏠 Home')
    
    # Welcome message
    st.write("""
    ## Welcome to Our Dashboard
    This is a multi-page application with authentication.
    """)
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Active Users",
            value="1,234",
            delta="↑ 123"
        )
        
        with st.expander("User Details"):
            st.write("""
            - Daily active users: 1,234
            - Monthly active users: 5,678
            - Year-over-year growth: 23%
            """)
            
    with col2:
        st.metric(
            label="Revenue",
            value="$12,345",
            delta="↑ 15%"
        )
        
        with st.expander("Revenue Breakdown"):
            st.write("""
            - Monthly recurring revenue: $10,000
            - One-time purchases: $2,345
            - Average revenue per user: $45
            """)
            
    with col3:
        st.metric(
            label="Engagement",
            value="89%",
            delta="↑ 2%"
        )
        
        with st.expander("Engagement Metrics"):
            st.write("""
            - Average session duration: 15 minutes
            - Pages per session: 4.5
            - Bounce rate: 25%
            """)
    
    # Additional content
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 View Full Reports"):
            st.write("Navigating to reports...")
            
    with col2:
        if st.button("⚙️ Account Settings"):
            st.write("Opening settings...")
