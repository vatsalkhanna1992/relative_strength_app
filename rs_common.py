import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import os


@st.cache_data(ttl=3600)
def get_price_from_csv(data_folder, ticker):
    """Get current and previous month-end prices from local CSV files."""
    try:
        file_path = os.path.join(data_folder, f"{ticker}.csv")
        if not os.path.exists(file_path):
            return None, None, None, None

        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        df = df.dropna(subset=['Date', 'Adj Close', 'Volume'])
        df = df.sort_values('Date')

        if len(df) < 2:
            return None, None, None, None

        current_price = df['Adj Close'].iloc[-1]
        current_volume = df['Volume'].iloc[-1]

        today = datetime.today()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)

        df_prev = df[df['Date'].dt.date <= last_month_end.date()].sort_values('Date')

        if len(df_prev) == 0:
            return None, None, None, None

        prev_price = df_prev['Adj Close'].iloc[-1]
        return current_price, prev_price, current_volume, df['Date'].iloc[-1]

    except Exception:
        return None, None, None, None


def _download_data_inline(all_tickers, data_folder):
    """Download stock data from Yahoo Finance with a visible progress bar."""
    import yfinance as yf

    os.makedirs(data_folder, exist_ok=True)

    start_date = "2020-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")

    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(all_tickers)
    all_data = []

    for i, ticker in enumerate(all_tickers):
        status_text.text(f"Downloading {ticker} ({i+1}/{total})...")
        try:
            df = yf.download(
                ticker, start=start_date, end=end_date,
                interval="1d", auto_adjust=False, progress=False,
            )
            if df.empty:
                continue
            df.reset_index(inplace=True)
            df.to_csv(os.path.join(data_folder, f"{ticker}.csv"), index=False)
            df["Ticker"] = ticker
            all_data.append(df)
        except Exception as e:
            status_text.text(f"Error downloading {ticker}: {e}")
        progress_bar.progress((i + 1) / total)

    if all_data:
        combined = pd.concat(all_data)
        combined.to_csv(os.path.join(data_folder, "ALL_COMBINED.csv"), index=False)

    progress_bar.empty()
    status_text.empty()
    st.success(f"Downloaded {len(all_data)}/{total} tickers successfully!")


def render_rs_dashboard(title, tickers, benchmark, data_folder, download_script):
    """Render a relative strength dashboard page.

    Args:
        title: Page title string
        tickers: List of stock tickers (excluding benchmark)
        benchmark: Benchmark ticker string
        data_folder: Absolute path to CSV data folder
        download_script: Filename of the download script (e.g. "data_download.py")
    """
    st.title(title)
    st.markdown("Stock prices vs. previous month end, ranked by Relative Strength (RS)")

    # Download & Refresh buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📥 Download Latest Data", key=f"download_{download_script}"):
            _download_data_inline(tickers + [benchmark], data_folder)
            st.cache_data.clear()
            st.rerun()
    with col_btn2:
        if st.button("🔄 Refresh Data", key=f"refresh_{download_script}"):
            st.cache_data.clear()
            st.rerun()

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Collect data
    data = []
    total_tickers = len(tickers) + 1  # +1 for benchmark

    for i, ticker in enumerate(tickers + [benchmark]):
        status_text.text(f"Loading {ticker}...")
        current_price, prev_price, volume, last_date = get_price_from_csv(data_folder, ticker)

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
        st.error(f"No data available. Please click 'Download Latest Data' or run {download_script} first.")
        st.stop()

    # Separate benchmark
    benchmark_row = df[df['Ticker'] == benchmark].iloc[0] if not df[df['Ticker'] == benchmark].empty else None
    df = df[df['Ticker'] != benchmark]

    # Calculate RS
    if benchmark_row is not None:
        bench_return = benchmark_row['Monthly Return (%)']
        df['RS (%)'] = df['Monthly Return (%)'] - bench_return
        df['RS Rank'] = df['RS (%)'].rank(ascending=False, method='first').astype(int)
    else:
        df['RS (%)'] = None
        df['RS Rank'] = None

    df = df.sort_values('RS Rank').reset_index(drop=True)

    st.info(f"📊 Loaded {len(df)} stocks out of {len(tickers)}")

    # Benchmark info
    if benchmark_row is not None:
        st.subheader("🏆 Benchmark Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{benchmark} Price", f"₹{benchmark_row['Current Price']:.2f}")
        with col2:
            st.metric("Monthly Return", f"{benchmark_row['Monthly Return (%)']:.2f}%")
        with col3:
            st.metric("Change", f"₹{benchmark_row['Change']:.2f}")

    # Top performers
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

    fig_rs = px.histogram(df, x='RS (%)', nbins=20, title="RS Distribution")
    st.plotly_chart(fig_rs, use_container_width=True)

    top_10_rs = df.head(10)
    fig_top = px.bar(top_10_rs, x='Ticker', y='RS (%)', title="Top 10 RS Stocks")
    st.plotly_chart(fig_top, use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("Data loaded from local CSV files. RS = Stock Monthly Return - Benchmark Monthly Return")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
