import yfinance as yf
import pandas as pd
import os
from datetime import datetime

midcap150_tickers = [
    "ABB.NS", "ACC.NS", "ABCAPITAL.NS", "APLAPOLLO.NS", "AUBANK.NS",
    "AUROPHARMA.NS", "DMART.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS",
    "BERGEPAINT.NS", "BHARATFORG.NS", "BIOCON.NS", "BSOFT.NS", "CANBK.NS",
    "CHOLAFIN.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CROMPTON.NS",
    "CUB.NS", "CUMMINSIND.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DIVISLAB.NS",
    "DIXON.NS", "ESCORTS.NS", "FEDERALBNK.NS", "FORTIS.NS", "GMRAIRPORT.NS",
    "GUJGASLTD.NS", "GODREJCP.NS", "GODREJPROP.NS", "HDFCAMC.NS", "HUDCO.NS",
    "IDFCFIRSTB.NS", "INDIANB.NS", "INDHOTEL.NS", "IGL.NS", "IRCTC.NS",
    "IRFC.NS", "JINDALSTEL.NS", "JSWENERGY.NS", "JUBLFOOD.NS", "KPITTECH.NS",
    "LICHSGFIN.NS", "LICI.NS", "LTIM.NS", "LTTS.NS", "LUPIN.NS",
    "MFSL.NS", "MARICO.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS",
    "MUTHOOTFIN.NS", "NAM-INDIA.NS", "NHPC.NS", "NMDC.NS", "OBEROIRLTY.NS",
    "OFSS.NS", "PAGEIND.NS", "PERSISTENT.NS", "PETRONET.NS", "PIIND.NS",
    "PFC.NS", "PNB.NS", "POLYCAB.NS", "PVRINOX.NS", "RECLTD.NS",
    "SAIL.NS", "SRF.NS", "SIEMENS.NS", "SJVN.NS", "SOLARINDS.NS",
    "SUNTV.NS", "SUPREMEIND.NS", "TATACOMM.NS", "TATAELXSI.NS", "TATAPOWER.NS",
    "TORNTPHARM.NS", "TVSMOTOR.NS", "UPL.NS", "VEDL.NS", "VOLTAS.NS",
    "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "PHOENIXLTD.NS", "HONAUT.NS",
    "IDEA.NS", "FACT.NS", "NLCINDIA.NS", "SUZLON.NS", "SONACOMS.NS",
    "KALYANKJIL.NS", "POLICYBZR.NS", "NYKAA.NS", "LLOYDSME.NS", "ASTRAL.NS",
    "INDUSTOWER.NS", "CGPOWER.NS", "KEI.NS", "DELHIVERY.NS", "TIINDIA.NS",
    "POONAWALLA.NS", "BSE.NS", "PAYTM.NS", "ABFRL.NS", "IIFL.NS",
    "THERMAX.NS", "SCHAEFFLER.NS", "GRINDWELL.NS", "SUMICHEM.NS", "IPCALAB.NS",
    "AFFLE.NS", "RATNAMANI.NS", "SYNGENE.NS", "SUVENPHAR.NS", "KAYNES.NS",
    "FIVESTAR.NS", "COCHINSHIP.NS", "CAMS.NS", "MAPMYINDIA.NS", "CDSL.NS",
    "METROBRAND.NS", "CLEAN.NS", "LATENTVIEW.NS", "HAPPSTMNDS.NS", "RKFORGE.NS",
    "MEDANTA.NS", "RAINBOW.NS", "CAMPUS.NS", "RATEGAIN.NS", "DATAPATTNS.NS",
    "JBMA.NS", "BIKAJI.NS", "RVNL.NS", "IREDA.NS",
    "MID150BEES.NS",
]

START_DATE = "2020-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")
OUTPUT_FOLDER = "midcap_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

all_data = []
for ticker in midcap150_tickers:
    try:
        print(f"Downloading {ticker}")
        df = yf.download(ticker, start=START_DATE, end=END_DATE, interval="1d", auto_adjust=False, progress=False)
        if df.empty:
            print(f"No data for {ticker}")
            continue
        df.reset_index(inplace=True)
        file_path = os.path.join(OUTPUT_FOLDER, f"{ticker}.csv")
        df.to_csv(file_path, index=False)
        df["Ticker"] = ticker
        all_data.append(df)
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

if all_data:
    combined_df = pd.concat(all_data)
    combined_df.to_csv(os.path.join(OUTPUT_FOLDER, "MIDCAP150_ALL.csv"), index=False)
    print("Combined CSV saved.")
print("Download Completed.")
