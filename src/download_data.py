from utils.paths import RAW_DATA_DIR
import requests
from datetime import datetime

import yfinance as yf
import pandas as pd

#raw data paths
RAW_OIL_FUTURES_DIR = RAW_DATA_DIR / "oil_futures"
RAW_OIL_FUTURES_DIR.mkdir(parents=True, exist_ok=True)

def download_oil_futures(start, end, interval):
    #NOTE: df stands for dataframe since yfinance download saves historical_data as a pandas dataframe
    oil_df = yf.download("CL=F", start=start, end=end, interval=interval, multi_level_index=False) #multi level index set to false to only get the indexes i need
    oil_df.to_csv(RAW_OIL_FUTURES_DIR / "oil_futures_daily.csv")

    print(f"Saved oil futures data with {len(oil_df)} rows")


RAW_BDTI_DIR = RAW_DATA_DIR / "bdti"
RAW_BDTI_DIR.mkdir(parents=True, exist_ok=True)

#NOTE:below is the failed attempt at scraping investing.com, unfortunately have to manually import the data for now 

#def download_BDTI(start, end):
#    url = "https://www.investing.com/indices/baltic-dirty-tanker-historical-data"
#    
#    headers = {
#        "User-Agent": "Mozilla/5.0"
#    }
#    
#    tables = pd.read_html(requests.get(url, headers=headers).text)
#    bdti_df = tables[0]
#    
#    bdti_df["Date"] = pd.to_datetime(bdti_df["Date"])
#    bdti_df = bdti_df[["Date", "Price"]].rename(columns={"Price": "BDTI"})
#    bdti_df = bdti_df.sort_values("Date")
#    
#    bdti_df.to_csv("data/raw/bdti/bdti_daily.csv", index=False)
#    print(f"Saved BDTI data with {len(bdti_df)} rows")

#NOTE: this idiom checks if a script is being run directly as the main program or being imported as a module into another script.
#      we make sure that the specified functions only run if its being ran directly from this program
if __name__ == "__main__":
    start = pd.to_datetime("2020-01-01")
    end = pd.to_datetime("2026-01-01")

    download_oil_futures(start, end, "1d")
    #download_BDTI(start, end)
