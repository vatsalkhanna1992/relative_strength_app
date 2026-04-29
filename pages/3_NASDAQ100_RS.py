import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from rs_common import render_rs_dashboard

# =========================
# NASDAQ 100 tickers (Yahoo Finance)
# No suffix needed for US stocks
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
    # Additional constituents
    "PDD", "SBUX", "MSTR", "TTD", "HOOD", "RBLX", "LYFT", "LCID", "RIVN",
    "CHKP", "SIRI", "ALGN", "EXPE", "VRSK", "MNST", "BMRN", "FAST", "ZBRA",
    "CDAY", "SPLK", "WBA",
]

# Remove duplicates while preserving order
seen = set()
nasdaq100_tickers = [t for t in nasdaq100_tickers if not (t in seen or seen.add(t))]

BENCHMARK = "QQQ"
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nasdaq100_data")

render_rs_dashboard(
    title="📈 NASDAQ 100 Relative Strength Dashboard",
    tickers=nasdaq100_tickers,
    benchmark=BENCHMARK,
    data_folder=DATA_FOLDER,
    download_script="data_download_nasdaq100.py",
)
