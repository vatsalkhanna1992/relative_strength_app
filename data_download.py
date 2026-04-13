import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# =========================
# NIFTY 50 Yahoo tickers
# (.NS is required for NSE)
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
    "ETERNAL.NS",
    "NIFTYBEES.NS",
]
# =========================
# Settings
# =========================

START_DATE = "2020-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")

OUTPUT_FOLDER = "nifty50_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# Download Data
# =========================

all_data = []

for ticker in nifty50_tickers:

    try:
        print(f"Downloading {ticker}")

        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"No data for {ticker}")
            continue

        df.reset_index(inplace=True)

        # Save individual CSV
        file_path = os.path.join(
            OUTPUT_FOLDER,
            f"{ticker}.csv"
        )

        df.to_csv(file_path, index=False)

        # Add ticker column for combined file
        df["Ticker"] = ticker
        all_data.append(df)

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

# =========================
# Save Combined CSV
# =========================

if all_data:

    combined_df = pd.concat(all_data)

    combined_df.to_csv(
        os.path.join(OUTPUT_FOLDER, "NIFTY50_ALL.csv"),
        index=False
    )

    print("Combined CSV saved.")

print("Download Completed.")