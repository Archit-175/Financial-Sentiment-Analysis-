import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from utils.model_utils import load_model, prepare_features, make_prediction

# Load the model at app startup
model = load_model()

# Set page configuration
"""st.set_page_config(
    page_title="Stock Analysis - Analysis",
    page_icon="📊",
    layout="wide"
)"""

# Title
st.markdown("<h1 class='title-text'>Stock Analysis 📊</h1>", unsafe_allow_html=True)

# Create two columns for input parameters
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Input Parameters 📝")
    
    # Date Selection
    selected_date = st.date_input(
        "Select Date 📅",
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now(),
        value=datetime.now(),
        help="Choose the date for stock analysis"
    )
    
    # RSI Input
    rsi_value = st.number_input(
        "RSI (Relative Strength Index) 📊",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        help="Enter RSI value between 0 and 100"
    )
    
    # ROC Input
    roc_value = st.number_input(
        "ROC (Rate of Change) 📈",
        value=0.0,
        help="Enter the Rate of Change value"
    )
    
    # Volume Input
    volume = st.number_input(
        "Volume 📊",
        min_value=0,
        value=1000000,
        help="Enter the trading volume"
    )
    
    # Analysis Button
    if st.button("Analyze ▶️", key="analyze_button"):
        if model is not None:
            with st.spinner("Analyzing data..."):
                # Prepare features
                features = prepare_features(selected_date, rsi_value, roc_value, volume)
                
                # Make prediction
                prediction = make_prediction(model, features)
                
                if prediction is not None:
                    # Store prediction in session state for visualization
                    st.session_state['prediction'] = prediction
                    st.session_state['features'] = features
                    
                    # Display prediction
                    st.success(f"Predicted Next Day Return: {prediction:.4f}")
        else:
            st.error("Model could not be loaded. Please check the model file.")

with col2:
    st.markdown("### Prediction Visualization 📈")
    
    # Create visualization if prediction exists
    if 'prediction' in st.session_state:
        # Generate future dates for prediction visualization
        future_dates = pd.date_range(start=selected_date, periods=10)
        
        # Create price trajectory based on prediction
        base_price = 100  # Starting price
        predicted_return = st.session_state['prediction']
        
        # Generate a price trajectory
        price_trajectory = [base_price]
        for i in range(1, 10):
            next_price = price_trajectory[-1] * (1 + predicted_return)
            price_trajectory.append(next_price)
        
        # Create the line chart using Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=price_trajectory,
            mode='lines+markers',
            name='Predicted Price',
            line=dict(color='#1976D2', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Predicted Stock Behavior",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display feature importance or additional metrics
        st.markdown("### Analysis Details")
        st.markdown(f"""
        **Input Features:**
        - RSI: {st.session_state['features']['RSI']:.2f}
        - ROC: {st.session_state['features']['ROC']:.2f}
        - Volume: {st.session_state['features']['Volume']:,.0f}
        """)
    
    # Additional Info Box
    st.info("""
    📌 **How to use:**
    1. Enter the required technical indicators
    2. Click 'Analyze' to get predictions
    3. View the predicted return and trend visualization
    """)