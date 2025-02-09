import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from utils.model_utils import load_model, prepare_features, make_prediction

# Load the model at app startup
model = load_model()

'''# Set page configuration
st.set_page_config(
    page_title="Stock Analysis - Analysis",
    page_icon="📊",
    layout="wide"
)'''

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
    
    # Current Price Input
    current_price_text = st.text_input(
        "Current Price 💲",
        value="100.0",
        help="Enter the current stock price"
    )
    try:
        current_price = float(current_price_text)
        if current_price <= 0:
            st.error("Price must be greater than 0")
    except ValueError:
        st.error("Please enter a valid number for Current Price")
        current_price = 100.0
    
    # RSI Input
    rsi_text = st.text_input(
        "RSI (Relative Strength Index) 📊",
        value="50.0",
        help="Enter RSI value between 0 and 100"
    )
    try:
        rsi_value = float(rsi_text)
        if not 0 <= rsi_value <= 100:
            st.error("RSI must be between 0 and 100")
    except ValueError:
        st.error("Please enter a valid number for RSI")
        rsi_value = 50.0
    
    # ROC Input
    roc_text = st.text_input(
        "ROC (Rate of Change) 📈",
        value="0.0",
        help="Enter the Rate of Change value"
    )
    try:
        roc_value = float(roc_text)
    except ValueError:
        st.error("Please enter a valid number for ROC")
        roc_value = 0.0
    
    # Volume Input
    volume_text = st.text_input(
        "Volume 📊",
        value="1000000",
        help="Enter the trading volume"
    )
    try:
        volume = float(volume_text)
        if volume < 0:
            st.error("Volume cannot be negative")
            volume = 0
    except ValueError:
        st.error("Please enter a valid number for Volume")
        volume = 0
    
    # Analysis Button
    if st.button("Analyze ▶️", key="analyze_button"):
        # Validate all inputs before proceeding
        if all([isinstance(rsi_value, float), 
                isinstance(roc_value, float), 
                isinstance(volume, float),
                isinstance(current_price, float)]) and 0 <= rsi_value <= 100 and volume >= 0 and current_price > 0:
            
            if model is not None:
                with st.spinner("Analyzing data..."):
                    # Prepare features
                    features = prepare_features(selected_date, rsi_value, roc_value, volume)
                    
                    # Make prediction
                    prediction = make_prediction(model, features)
                    
                    if prediction is not None:
                        # Store prediction and current price in session state for visualization
                        st.session_state['prediction'] = prediction
                        st.session_state['features'] = features
                        st.session_state['current_price'] = current_price
                        
                        # Display prediction in decimal format
                        st.success(f"Predicted Next Day Return: {prediction}")
            else:
                st.error("Model could not be loaded. Please check the model file.")
        else:
            st.error("Please correct the input values before analyzing")

with col2:
    st.markdown("### Prediction Visualization 📈")
    
    # Create visualization if prediction exists
    if 'prediction' in st.session_state:
        # Generate dates for visualization
        current_date = datetime.strptime("2025-02-09 10:44:55", "%Y-%m-%d %H:%M:%S")  # Current UTC time
        future_dates = pd.date_range(start=current_date, periods=10, freq='D')
        
        # Create price trajectories
        predicted_return = st.session_state['prediction']
        current_price = st.session_state['current_price']
        
        # Generate current price trajectory (flat line)
        current_trajectory = [current_price] * len(future_dates)
        
        # Generate predicted price trajectory
        predicted_trajectory = [current_price]
        for i in range(1, len(future_dates)):
            next_price = predicted_trajectory[-1] * (1 + predicted_return)
            predicted_trajectory.append(next_price)
        
        # Create the line chart using Plotly
        fig = go.Figure()
        
        # Add current price line
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=current_trajectory,
            mode='lines',
            name='Current Price',
            line=dict(color='#4CAF50', width=2, dash='dash'),
        ))
        
        # Add predicted price line
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=predicted_trajectory,
            mode='lines+markers',
            name='Predicted Price',
            line=dict(color='#1976D2', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Stock Price Prediction",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            height=400,
            showlegend=True,
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Add current date/time and user annotation
        fig.add_annotation(
            text=f"Analysis Time (UTC): 2025-02-09 10:44:55\nUser: Archit-175",
            xref="paper",
            yref="paper",
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            showarrow=False,
            font=dict(size=10),
            align="right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display analysis details
        st.markdown("### Analysis Details")
        st.markdown(f"""
        **Input Features:**
        - Current Price: {st.session_state['current_price']}
        - RSI: {st.session_state['features']['RSI']}
        - ROC: {st.session_state['features']['ROC']}
        - Volume: {st.session_state['features']['Volume']}
        - Predicted Return: {st.session_state['prediction']}
        
        **Analysis Information:**
        - Analysis Time (UTC): 2025-02-09 10:44:55
        - User: Archit-175
        """)
    
    # Additional Info Box
    st.info("""
    📌 **How to use:**
    1. Enter the current stock price and technical indicators
    2. Click 'Analyze' to get predictions
    3. View both current and predicted price trends
    """)
