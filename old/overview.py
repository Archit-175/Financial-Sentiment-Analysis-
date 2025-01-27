import streamlit as st

# Fundamental Analysis Page
st.title("Fundamental Analysis")
st.markdown("""
Analyze stocks' intrinsic value based on key financial indicators like:
- **Earnings Per Share (EPS)**: Profit allocated to each outstanding share.
- **Price-to-Earnings Ratio (P/E Ratio)**: Valuation ratio, shows how expensive a stock is relative to earnings.
- **Dividend Yield**: Measures the annual dividend payment relative to the stock price.
""")

# Sidebar input (optional for more functionality)
st.sidebar.header("Input Data")
EPS = st.sidebar.number_input("Earnings Per Share (EPS)", min_value=0.0, step=0.1)
PE_Ratio = st.sidebar.number_input("P/E Ratio", min_value=0.0, step=0.1)
Dividend_Yield = st.sidebar.number_input("Dividend Yield (%)", min_value=0.0, step=0.1)
