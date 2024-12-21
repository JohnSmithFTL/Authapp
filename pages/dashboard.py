# File: pages/dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_sample_data():
    # Generate sample data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 100, len(dates)),
        'visitors': np.random.normal(500, 50, len(dates)),
        'conversion': np.random.uniform(0.1, 0.3, len(dates))
    }
    return pd.DataFrame(data)

def app(username):
    st.title('📊 Dashboard')
    
    # Sidebar filters
    st.sidebar.subheader("Filters")
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )
    
    # Load and filter data
    df = generate_sample_data()
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Sales",
            f"${df['sales'].sum():,.0f}",
            f"{df['sales'].pct_change().mean()*100:+.1f}%"
        )
        
    with col2:
        st.metric(
            "Total Visitors",
            f"{df['visitors'].sum():,.0f}",
            f"{df['visitors'].pct_change().mean()*100:+.1f}%"
        )
        
    with col3:
        st.metric(
            "Avg Conversion Rate",
            f"{df['conversion'].mean()*100:.1f}%",
            f"{df['conversion'].pct_change().mean()*100:+.1f}%"
        )
    
    # Charts
    st.subheader("Sales Overview")
    
    # Sales trend
    fig_sales = px.line(
        df,
        x='date',
        y='sales',
        title='Daily Sales Trend'
    )
    st.plotly_chart(fig_sales, use_container_width=True)
    
    # Visitors vs Conversion
    fig_conversion = go.Figure()
    fig_conversion.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['visitors'],
            name='Visitors',
            line=dict(color='blue')
        )
    )
    fig_conversion.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['conversion']*100,
            name='Conversion Rate (%)',
            line=dict(color='green'),
            yaxis='y2'
        )
    )
    fig_conversion.update_layout(
        title='Visitors and Conversion Rate',
        yaxis=dict(title='Visitors'),
        yaxis2=dict(title='Conversion Rate (%)', overlaying='y', side='right')
    )
    st.plotly_chart(fig_conversion, use_container_width=True)
    
    # Data table
    st.subheader("Detailed Data")
    st.dataframe(
        df.set_index('date').style.format({
            'sales': '${:,.2f}',
            'visitors': '{:,.0f}',
            'conversion': '{:.1%}'
        })
    )
