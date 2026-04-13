import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ProStock Analytics", layout="wide")

st.title("📊 ProStock Real-Time Dashboard")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Navigation")
ticker = st.sidebar.text_input("Enter Ticker Symbol", "AAPL").upper()
time_period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "5y", "max"])

# API Call
API_URL = f"http://localhost:8000/api/stock/{ticker}?period={time_period}"

if st.sidebar.button("Fetch Data"):
    with st.spinner("Analyzing Market Data..."):
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data["history"])
            info = data["info"]

            # Layout: Stats & Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Company", info["name"])
            col2.metric("Current Price", f"${info['current_price']}")
            col3.metric("Sector", info["sector"])

            st.write(f"**Business Summary:** {info['summary']}")

            # Advanced Charting: Candlestick
            fig = go.Figure(data=[go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Price"
            )])
            
            fig.update_layout(
                title=f"{ticker} Price Action",
                yaxis_title="Stock Price (USD)",
                template="plotly_dark",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Raw Data View
            with st.expander("View Raw Historical Data"):
                st.dataframe(df)
        else:
            st.error("Error: Could not fetch data. Check the ticker symbol.")
