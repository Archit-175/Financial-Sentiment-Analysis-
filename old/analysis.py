'''import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# Load the trained model
@st.cache_resource
def load_model():
    model_path = "APP\pages\model.pkl"  # Update this if the file is in a different directory
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()  # Stop execution if the model file is missing

# Technical Analysis Page
st.title("Technical Analysis")

# Sidebar input section
st.sidebar.header("Input Features")
RSI = st.sidebar.number_input("RSI", min_value=0.0, max_value=100.0, step=0.1)
ROC = st.sidebar.number_input("ROC", min_value=-50.0, max_value=50.0, step=0.1)
VOLUME = st.sidebar.number_input("Volume", min_value=0.0, max_value=1000000000.0, step=1000.0)

# Predict button and model-based prediction
if st.sidebar.button("Predict"):
    input_data = pd.DataFrame({
        "RSI": [RSI],
        "ROC": [ROC],
        "Volume": [VOLUME]
    })

    # Use the trained model for prediction
    try:
        prediction = model.predict(input_data)
        st.success(f"Predicted Next Day Return: {prediction[0]:.2f}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")'''

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# Load the trained model
@st.cache_resource
def load_model():
    model_path = "APP\pages\model.pkl"  # Update this if the file is in a different directory
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()  # Stop execution if the model file is missing

# Technical Analysis Page
st.title("Technical Analysis")

# Sidebar input section
st.sidebar.header("Input Features")
RSI = st.sidebar.number_input("RSI", min_value=0.0, max_value=100.0, step=0.1)
ROC = st.sidebar.number_input("ROC", min_value=-50.0, max_value=50.0, step=0.1)
VOLUME = st.sidebar.number_input("Volume", min_value=0.0, max_value=1000000000.0, step=1.0)

# Predict button and model-based prediction
if st.sidebar.button("Predict"):
    input_data = pd.DataFrame({
        "RSI": [RSI],
        "ROC": [ROC],
        "Volume": [VOLUME]
    })

    # Use the trained model for prediction
    try:
        prediction = model.predict(input_data)
        st.success(f"Predicted Next Day Return: {prediction[0]:.2f}")

        # Create trend data for visualization
        trend_data = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=10),
            "Actual": np.random.randn(10).cumsum(),
            "Predicted": np.cumsum([prediction[0]] * 10)
        })

        # Plot the trend
        st.write("### Return Trends")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(trend_data["Date"], trend_data["Actual"], label="Actual", color="blue")
        ax.plot(trend_data["Date"], trend_data["Predicted"], label="Predicted", color="orange", linestyle="--")
        ax.set_title("Return Trends")
        ax.set_xlabel("Date")
        ax.set_ylabel("Returns")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error in prediction: {e}")