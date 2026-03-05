from pathlib import Path

import yfinance as yf

#setup path to a data folder
DATA_PATH = Path(__file__).resolve().parents[1]

#raw data paths
RAW_PATH = DATA_PATH / "data" / "raw"
OIL_FUTURES_PATH = RAW_PATH / "oil_futures"

OIL_FUTURES_PATH.mkdir(parents=True, exist_ok=True)

#processed data paths
PROCESSED_PATH = DATA_PATH / "data" / "processed"



def download_oil_futures(start, end, interval):
    #NOTE: df stands for dataframe since yfinance download saves historical_data as a pandas dataframe
    df = yf.download("CL=F", start=start, end=end, interval=interval)
    df.to_csv(OIL_FUTURES_PATH / "oil_futures.csv")

    print(df.head())




#NOTE: this idiom checks if a script is being run directly as the main program or being imported as a module into another script.
#      we make sure that the specified functions only run if its being ran directly from this program
if __name__ == "__main__":
    download_oil_futures("2020-01-01", "2026-01-01", "1d")
