import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="S&P 500 Dashboard", layout="wide")

st.title("📈 S&P 500 Yahoo Finance Dashboard")
st.write("View live charts, historical performance, and key statistics for the S&P 500 (^GSPC).")

# Sidebar settings
st.sidebar.header("Configuration")
ticker_symbol = "^GSPC"

# Date selectors
today = datetime.date.today()
five_years_ago = today - datetime.timedelta(days=365*5)
start_date = st.sidebar.date_input("Start Date", five_years_ago)
end_date = st.sidebar.date_input("End Date", today)

# Fetch data
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

try:
    df = load_data(ticker_symbol, start_date, end_date)
    
    if df.empty:
        st.error("No data found for the selected date range.")
    else:
        # Format index to display dates cleanly
        df.index = df.index.date

        # Summary Metric Blocks
        col1, col2, col3, col4 = st.columns(4)
        latest_close = float(df['Close'].iloc[-1])
        previous_close = float(df['Close'].iloc[-2])
        change = latest_close - previous_close
        pct_change = (change / previous_close) * 100

        col1.metric("Latest Close", f"{latest_close:,.2f} USD")
        col2.metric("Daily Change", f"{change:+,.2f} USD", f"{pct_change:+.2f}%")
        col3.metric("Period High", f"{float(df['High'].max()):,.2f} USD")
        col4.metric("Period Low", f"{float(df['Low'].min()):,.2f} USD")

        # Interactive Chart using Plotly
        st.subheader("Interactive Historical Performance Chart")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'].values.flatten(),
            mode='lines',
            name='S&P 500 Close',
            line=dict(color='#008080', width=2)
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Close Price (USD)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.3)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show Raw Data option
        if st.checkbox("Show Raw Data Table"):
            st.write(df)
            
except Exception as e:
    st.error(f"An error occurred while fetching data: {e}")
