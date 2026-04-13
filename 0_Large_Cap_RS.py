import os
import sys

# Add project root to path so pages can import rs_common
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rs_common import render_rs_dashboard

# =========================
# NIFTY 50 Yahoo tickers
# =========================

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
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nifty50_data")

render_rs_dashboard(
    title="📈 Nifty 50 Relative Strength Dashboard (Large Cap)",
    tickers=nifty50_tickers,
    benchmark=BENCHMARK,
    data_folder=DATA_FOLDER,
    download_script="data_download.py",
)
