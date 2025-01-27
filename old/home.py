import streamlit as st

# Welcome page content
st.title("Welcome to Financial Analysis")
st.markdown("""
### This application provides insights into financial data:
- **Technical Analysis**: Analyze historical price trends and patterns.
- **Fundamental Analysis**: Evaluate the intrinsic value of stocks.
- **Sentiment Analysis**: Predict market movements based on news and trends.

#### Purpose:
This app is designed for financial analysts, traders, and enthusiasts to gain actionable insights.

#### Key Financial Terms:
- **RSI**: Relative Strength Index, used to measure momentum.
- **ROC**: Rate of Change, a momentum indicator.
- **Moving Avg**: Simple moving average of stock prices.

### Navigation:
Use the sidebar to switch between different pages such as **Technical Analysis**, **Fundamental Analysis**, and **Sentiment Analysis**.

""")

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("""
- [Home](#)
- [Technical Analysis](#)
- [Fundamental Analysis](#)
""")
