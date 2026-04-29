import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# =========================
# NASDAQ 100 Yahoo tickers
# (No suffix needed for US stocks)
# =========================

nasdaq100_tickers = [
    # Mega-cap tech
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "AVGO", "COST",
    # Large-cap tech & growth
    "NFLX", "AMD", "ASML", "CSCO", "TMUS", "QCOM", "AMGN", "INTU", "ADBE", "TXN",
    "MU", "AMAT", "ISRG", "BKNG", "KLAC", "LRCX", "REGN", "MELI", "SNPS", "ADI",
    "CDNS", "MDLZ", "GILD", "VRTX", "CSX", "CTAS", "MRVL", "PANW", "ORLY", "ROST",
    "MCHP", "IDXX", "CRWD", "DXCM", "MNST", "BIIB", "TEAM", "PAYX", "FAST", "ODFL",
    "ANSS", "PCAR", "NXPI", "DLTR", "WDAY", "ON", "DDOG", "APP", "CEG", "FANG",
    "CPRT", "GEHC", "TTWO", "VRSK", "CDW", "ENPH", "ROP", "CSGP", "NTAP",
    "PYPL", "EBAY", "CMCSA", "EA", "INTC", "LULU", "MAR", "FTNT", "ZS",
    "OKTA", "ABNB", "MRNA", "MDB", "SMCI", "GFS", "CCEP", "ILMN", "XEL", "EXC",
    "KHC", "WBD", "AZN", "LIN", "PEP", "HON",
    "PDD", "SBUX", "MSTR", "TTD", "HOOD", "RBLX", "LYFT", "LCID", "RIVN",
    "CHKP", "SIRI", "ALGN", "EXPE", "MNST", "BMRN", "FAST", "ZBRA",
    "CDAY", "SPLK", "WBA",
    # Benchmark ETF
    "QQQ",
]

# Remove duplicates while preserving order
seen = set()
nasdaq100_tickers = [t for t in nasdaq100_tickers if not (t in seen or seen.add(t))]

# =========================
# Settings
# =========================

START_DATE = "2020-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")

OUTPUT_FOLDER = "nasdaq100_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# Download Data
# =========================

all_data = []

for ticker in nasdaq100_tickers:
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

        # Flatten MultiIndex columns (yfinance >= 1.0 returns MultiIndex)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.reset_index(inplace=True)

        file_path = os.path.join(OUTPUT_FOLDER, f"{ticker}.csv")
        df.to_csv(file_path, index=False)

        df["Ticker"] = ticker
        all_data.append(df)

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

# =========================
# Save Combined CSV
# =========================

if all_data:
    combined_df = pd.concat(all_data)
    combined_df.to_csv(os.path.join(OUTPUT_FOLDER, "NASDAQ100_ALL.csv"), index=False)
    print("Combined CSV saved.")

print("Download Completed.")
