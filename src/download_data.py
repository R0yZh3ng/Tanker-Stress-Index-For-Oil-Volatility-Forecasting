from utils.paths import RAW_DATA_DIR

import yfinance as yf
import pandas as pd

#raw data paths
RAW_OIL_FUTURES_DIR = RAW_DATA_DIR / "oil_futures"
RAW_OIL_FUTURES_DIR.mkdir(parents=True, exist_ok=True)

def download_oil_futures(start, end, interval):
    #NOTE: df stands for dataframe since yfinance download saves historical_data as a pandas dataframe
    df = yf.download("CL=F", start=start, end=end, interval=interval, multi_level_index=False) #multi level index set to false to only get the indexes i need
    df.to_csv(RAW_OIL_FUTURES_DIR / "oil_futures_daily.csv")

    print(df.head())




#NOTE: this idiom checks if a script is being run directly as the main program or being imported as a module into another script.
#      we make sure that the specified functions only run if its being ran directly from this program
if __name__ == "__main__":
    download_oil_futures("2020-01-01", "2026-01-01", "1d")
