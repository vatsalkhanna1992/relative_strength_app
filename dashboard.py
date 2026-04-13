import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import subprocess
import sys
import os

# =========================
# NIFTY 50 Yahoo tickers
# (.NS is required for NSE)
# =========================

# nifty50_tickers = [
#     "ADANIENT.NS",
#     "ADANIPORTS.NS",
#     "APOLLOHOSP.NS",
#     "ASIANPAINT.NS",
#     "AXISBANK.NS",
#     "BAJAJ-AUTO.NS",
#     "BAJAJFINSV.NS",
#     "BAJFINANCE.NS",
#     "BEL.NS",
#     "BHARTIARTL.NS",
#     "BPCL.NS",
#     "BRITANNIA.NS",
#     "CIPLA.NS",
#     "COALINDIA.NS",
#     "DRREDDY.NS",
#     "EICHERMOT.NS",
#     "GRASIM.NS",
#     "HCLTECH.NS",
#     "HDFCBANK.NS",
#     "HDFCLIFE.NS",
#     "HEROMOTOCO.NS",
#     "HINDALCO.NS",
#     "HINDUNILVR.NS",
#     "ICICIBANK.NS",
#     "INDUSINDBK.NS",
#     "INFY.NS",
#     "ITC.NS",
#     "JIOFIN.NS",
#     "JSWSTEEL.NS",
#     "KOTAKBANK.NS",
#     "LT.NS",
#     "M&M.NS",
#     "MARUTI.NS",
#     "NESTLEIND.NS",
#     "NTPC.NS",
#     "ONGC.NS",
#     "POWERGRID.NS",
#     "RELIANCE.NS",
#     "SHRIRAMFIN.NS",
#     "SBILIFE.NS",
#     "SBIN.NS",
#     "SUNPHARMA.NS",
#     "TATACONSUM.NS",
#     "TATASTEEL.NS",
#     "TCS.NS",
#     "TECHM.NS",
#     "TITAN.NS",
#     "TMCV.NS",
#     "TRENT.NS",
#     "ULTRACEMCO.NS",
#     "ETERNAL.NS",
#     "WIPRO.NS",
# ]

nifty50_tickers = [
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BEL.NS",
    "BHARTIARTL.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "INFY.NS",
    "INDIGO.NS",
    "ITC.NS",
    "JIOFIN.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "M&M.NS",
    "MARUTI.NS",
    "MAXHEALTH.NS",
    "NESTLEIND.NS",
    "NTPC.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBILIFE.NS",
    "SHRIRAMFIN.NS",
    "SBIN.NS",
    "SUNPHARMA.NS",
    "TCS.NS",
    "TATACONSUM.NS",
    "TMCV.NS",
    "TATASTEEL.NS",
    "TECHM.NS",
    "TITAN.NS",
    "TRENT.NS",
    "ULTRACEMCO.NS",
    "WIPRO.NS",
    "ETERNAL.NS"
]

BENCHMARK = "NIFTYBEES.NS"
# Use absolute path for data folder
DATA_FOLDER = "/Users/vatsalkhanna1992/Projects/ai/stocks/relative_strength_app/nifty50_data"

# =========================
# Helper Functions
# =========================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_price_from_csv(ticker):
    """Get current and previous month-end prices from local CSV files."""
    try:
        file_path = os.path.join(DATA_FOLDER, f"{ticker}.csv")
        if not os.path.exists(file_path):
            return None, None, None, None
        
        df = pd.read_csv(file_path)
        
        # Convert Date column and handle parse errors
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Convert numeric columns, replacing any non-numeric values with NaN
        df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
        # Remove rows with NaN dates or prices
        df = df.dropna(subset=['Date', 'Adj Close', 'Volume'])
        df = df.sort_values('Date')
        
        if len(df) < 2:
            return None, None, None, None
        
        # Current price (latest)
        current_price = df['Adj Close'].iloc[-1]
        current_volume = df['Volume'].iloc[-1]
        
        # Previous month-end price
        today = datetime.today()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        
        # Find price on or near last month end
        df_prev = df[df['Date'].dt.date <= last_month_end.date()].sort_values('Date')
        
        if len(df_prev) == 0:
            return None, None, None, None
        
        prev_price = df_prev['Adj Close'].iloc[-1]
        
        return current_price, prev_price, current_volume, df['Date'].iloc[-1]
        
    except Exception as e:
        return None, None, None, None

# =========================
# Main Dashboard
# =========================

st.title("📈 Nifty 50 Relative Strength Dashboard")
st.markdown("Stock prices vs. previous month end, ranked by Relative Strength (RS)")

# Download & Refresh buttons
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📥 Download Latest Data"):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_download.py")
        with st.spinner("Downloading latest data from Yahoo Finance... This may take a minute."):
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
            )
        if result.returncode == 0:
            st.success("Data downloaded successfully!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error(f"Download failed:\n{result.stderr}")
with col_btn2:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Progress bar
progress_bar = st.progress(0)
status_text = st.empty()

# Collect data
data = []
total_tickers = len(nifty50_tickers) + 1  # +1 for benchmark

for i, ticker in enumerate(nifty50_tickers + [BENCHMARK]):
    status_text.text(f"Loading {ticker}...")
    
    current_price, prev_price, volume, last_date = get_price_from_csv(ticker)
    
    if current_price is not None and prev_price is not None:
        monthly_return = (current_price - prev_price) / prev_price * 100
        data.append({
            'Ticker': ticker,
            'Current Price': round(current_price, 2),
            'Prev Month Price': round(prev_price, 2),
            'Monthly Return (%)': round(monthly_return, 2),
            'Volume': int(volume) if volume else 0,
            'Change': round(current_price - prev_price, 2),
            'Last Updated': last_date
        })
    
    progress_bar.progress((i + 1) / total_tickers)

progress_bar.empty()
status_text.empty()

# Create DataFrame
df = pd.DataFrame(data)

if len(df) == 0:
    st.error("No data available. Please run data_download.py first.")
    st.stop()

# Separate benchmark
benchmark_row = df[df['Ticker'] == BENCHMARK].iloc[0] if not df[df['Ticker'] == BENCHMARK].empty else None
df = df[df['Ticker'] != BENCHMARK]

# Calculate RS (Relative Strength)
if benchmark_row is not None:
    bench_return = benchmark_row['Monthly Return (%)']
    df['RS (%)'] = df['Monthly Return (%)'] - bench_return
    df['RS Rank'] = df['RS (%)'].rank(ascending=False, method='dense').astype(int)
else:
    df['RS (%)'] = None
    df['RS Rank'] = None

# Sort by RS Rank
df = df.sort_values('RS Rank').reset_index(drop=True)

# Display info
st.info(f"📊 Loaded {len(df)} stocks out of {len(nifty50_tickers)}")

# Display benchmark info
if benchmark_row is not None:
    st.subheader("🏆 Benchmark Performance")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("NIFTYBEES.NS Price", f"₹{benchmark_row['Current Price']:.2f}")
    with col2:
        st.metric("Monthly Return", f"{benchmark_row['Monthly Return (%)']:.2f}%")
    with col3:
        st.metric("Change", f"₹{benchmark_row['Change']:.2f}")

# Display top performers
st.subheader("🚀 Top Momentum Stocks")
top_5 = df.head(5)
for _, row in top_5.iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            st.write(f"**{row['Ticker']}**")
        with col2:
            st.metric("Price", f"₹{row['Current Price']:.2f}", f"{row['Monthly Return (%)']:.2f}%")
        with col3:
            st.metric("RS", f"{row['RS (%)']:.2f}%", f"Rank #{row['RS Rank']}")
        with col4:
            st.metric("Volume", f"{row['Volume']:,}")

# Full table
st.subheader("📊 Complete Rankings")
st.dataframe(
    df[['RS Rank', 'Ticker', 'Current Price', 'Prev Month Price', 'Monthly Return (%)', 'RS (%)', 'Change', 'Volume']],
    use_container_width=True,
    column_config={
        "RS Rank": st.column_config.NumberColumn("Rank", format="%d"),
        "Current Price": st.column_config.NumberColumn("Current Price", format="₹%.2f"),
        "Prev Month Price": st.column_config.NumberColumn("Prev Month Price", format="₹%.2f"),
        "Monthly Return (%)": st.column_config.NumberColumn("Monthly Return", format="%.2f%%"),
        "RS (%)": st.column_config.NumberColumn("RS vs Benchmark", format="%.2f%%"),
        "Change": st.column_config.NumberColumn("Change", format="₹%.2f"),
        "Volume": st.column_config.NumberColumn("Volume", format="%d"),
    }
)

# Charts
st.subheader("📈 Visualizations")

# RS Distribution
fig_rs = px.histogram(df, x='RS (%)', nbins=20, title="RS Distribution")
st.plotly_chart(fig_rs, use_container_width=True)

# Top 10 RS
top_10_rs = df.head(10)
fig_top = px.bar(top_10_rs, x='Ticker', y='RS (%)', title="Top 10 RS Stocks")
st.plotly_chart(fig_top, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data loaded from local CSV files. RS = Stock Monthly Return - Benchmark Monthly Return")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
