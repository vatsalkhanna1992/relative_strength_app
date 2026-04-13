import os
import sys

# Add project root to path so pages can import rs_common
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rs_common import render_rs_dashboard

# =========================
# Nifty Midcap 150 tickers (Official list - April 2026)
# =========================

midcap150_tickers = [
    "ABCAPITAL.NS", "3MINDIA.NS", "ACC.NS", "AIAENG.NS", "APOLLOTYRE.NS",
    "ASHOKLEY.NS", "AUROPHARMA.NS", "LINDEINDIA.NS", "BANKINDIA.NS", "BERGEPAINT.NS",
    "BHARATFORG.NS", "BIOCON.NS", "CARBORUNIV.NS", "COLPAL.NS", "CONCOR.NS",
    "COROMANDEL.NS", "CRISIL.NS", "CGPOWER.NS", "CUMMINSIND.NS", "EMAMILTD.NS",
    "ESCORTS.NS", "EXIDEIND.NS", "SCHAEFFLER.NS", "FEDERALBNK.NS", "FORTIS.NS",
    "GLAXO.NS", "GMRAIRPORT.NS", "GODREJIND.NS", "GODREJPROP.NS", "FLUOROCHEM.NS",
    "GUJGASLTD.NS", "HINDPETRO.NS", "HINDZINC.NS", "HONAUT.NS", "IDBI.NS",
    "IDEA.NS", "INDIANB.NS", "INDHOTEL.NS", "IOB.NS", "IGL.NS",
    "IPCALAB.NS", "IRB.NS", "JSL.NS", "JUBLFOOD.NS", "LICHSGFIN.NS",
    "LUPIN.NS", "M&MFIN.NS", "MARICO.NS", "MFSL.NS", "MPHASIS.NS",
    "MRF.NS", "MRPL.NS", "NLCINDIA.NS", "NMDC.NS", "OBEROIRLTY.NS",
    "OIL.NS", "OFSS.NS", "PAGEIND.NS", "PERSISTENT.NS", "PETRONET.NS",
    "PHOENIXLTD.NS", "PRESTIGE.NS", "PGHH.NS", "PATANJALI.NS", "SKFINDIA.NS",
    "SRF.NS", "SAIL.NS", "SUNTV.NS", "SUNDARMFIN.NS", "SUNDRMFAST.NS",
    "SUPREMEIND.NS", "SUZLON.NS", "TATACHEM.NS", "TATACOMM.NS", "TATAELXSI.NS",
    "TATAINVEST.NS", "THERMAX.NS", "TORNTPOWER.NS", "UBL.NS", "UPL.NS",
    "VOLTAS.NS", "YESBANK.NS", "ABBOTINDIA.NS", "BAYERCROP.NS", "INDUSTOWER.NS",
    "BALKRISIND.NS", "MAHABANK.NS", "JKCEMENT.NS", "LTF.NS", "POONAWALLA.NS",
    "MUTHOOTFIN.NS", "COFORGE.NS", "SJVN.NS", "SOLARINDS.NS", "TIMKEN.NS",
    "ZFCVINDIA.NS", "PIIND.NS", "FACT.NS", "ABSLAMC.NS", "ASTRAL.NS",
    "APLAPOLLO.NS", "GRINDWELL.NS", "UNOMINDA.NS", "DEEPAKNTR.NS", "KEI.NS",
    "AJANTPHARM.NS", "DALBHARAT.NS", "KPRMILL.NS", "SYNGENE.NS", "IDFCFIRSTB.NS",
    "ALKEM.NS", "LTTS.NS", "ENDURANCE.NS", "BSE.NS", "HUDCO.NS",
    "AUBANK.NS", "COCHINSHIP.NS", "DIXON.NS", "GICRE.NS", "NAM-INDIA.NS",
    "NIACL.NS", "TIINDIA.NS", "BANDHANBNK.NS", "BDL.NS", "HDFCAMC.NS",
    "RVNL.NS", "POLYCAB.NS", "KPITTECH.NS", "SBICARD.NS", "POWERINDIA.NS",
    "MAXHEALTH.NS", "MAZDOCK.NS", "GLAND.NS", "KALYANKJIL.NS", "SONACOMS.NS",
    "POLICYBZR.NS", "PAYTM.NS", "NYKAA.NS", "STARHEALTH.NS", "METROBRAND.NS",
    "AWL.NS", "MOTHERSON.NS", "DELHIVERY.NS", "MEDANTA.NS", "MANKIND.NS",
    "TATATECH.NS", "LLOYDSME.NS", "JSWINFRA.NS", "IREDA.NS", "BHARTIHEXA.NS"
]

BENCHMARK = "MID150BEES.NS"
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "midcap_data")

render_rs_dashboard(
    title="Nifty Midcap 150 Relative Strength Dashboard (Mid Cap)",
    tickers=midcap150_tickers,
    benchmark=BENCHMARK,
    data_folder=DATA_FOLDER,
    download_script="data_download_midcap.py",
)