import os
import glob
import yfinance as yf
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_FUTURE_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "futures")
RAW_FLARE_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "flares")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

os.makedirs(RAW_FUTURE_DATA_DIR, exist_ok = True)
os.makedirs(RAW_FLARE_DATA_DIR, exist_ok = True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok = True)

def download_wti(start_date, end_date):
    print(f"Downloading WTI Crude Oil Futures data from {start_date} to {end_date}")
    oil = yf.download("CL=F", start = start_date, end = end_date)
    oil['Returns'] = oil['Close'].pct_change()
    oil['Volatility-20d'] = oil['Returns'].rolling(20).std() * (252 ** 0.5)

    file_path = os.path.join(RAW_FUTURE_DATA_DIR, "wti_oil_raw.csv")
    oil.to_csv(file_path)
    print(f"WTI data saved to {file_path}")
    return file_path

def concatenate():
    flare_files = sorted(glob.glob(os.path.join(RAW_FLARE_DATA_DIR, "*_flare_list.csv")))
    flare_dfs = [pd.read_csv(f) for f in flare_files]
    flares = pd.concat(flare_dfs, ignore_index=True)
    
    flares['date'] = pd.to_datetime(flares['acq_date'])
    daily_flares = flares.groupby('date').size().reset_index(name='flare_count')
    
    oil_csv_path = os.path.join(RAW_FUTURE_DATA_DIR, "wti_oil_raw.csv")
    oil = pd.read_csv(oil_csv_path)
    oil['Date'] = pd.to_datetime(oil['Date'])
    
    merged = pd.merge(oil, daily_flares, left_on='Date', right_on='date', how='left')
    merged['flare_count'] = merged['flare_count'].fillna(0)
    merged.drop(columns=['date'], inplace=True)

    merged_csv_path = os.path.join(PROCESSED_DATA_DIR, "merged_oil_flares.csv")
    merged.to_csv(merged_csv_path, index=False)
    
    print(f"Merged dataset saved to {merged_csv_path}")
    print(merged.head())

if __name__ == "__main__":
    download_wti("2012-01-01", "2019-12-31")
    concatenate()
