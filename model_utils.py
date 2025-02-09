import pickle
import os
from pathlib import Path
import streamlit as st
import numpy as np

# Get the current working directory
current_dir = Path.cwd()

# Define the model directory and path relative to the current directory
MODEL_DIR = current_dir / "model"
MODEL_PATH = MODEL_DIR / "stock_model.pkl"

@st.cache_resource
def load_model():
    """Load the trained model from pickle file"""
    try:
        # Create model directory if it doesn't exist
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        
        if MODEL_PATH.exists():
            with open(MODEL_PATH, 'rb') as file:
                model = pickle.load(file)
            return model
        else:
            st.error(f"Model file not found at {MODEL_PATH}. Please ensure the model file exists in the correct location.")
            return None
    
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def prepare_features(date, rsi, roc, volume):
    """Prepare features for model prediction"""
    features = {
        'RSI': float(rsi),
        'ROC': float(roc),
        'Volume': float(volume)
    }
    return features

def make_prediction(model, features):
    """Make prediction using the loaded model"""
    try:
        # Convert features to the format expected by the model
        feature_values = np.array([list(features.values())])
        prediction = model.predict(feature_values)
        return prediction[0]
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None