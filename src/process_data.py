import numpy as np
import pandas as pd

from utils.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

#processed data paths
PROCESSED_OIL_FUTURES_DIR = PROCESSED_DATA_DIR / "oil_futures"
PROCESSED_OIL_FUTURES_DIR.mkdir(parents=True, exist_ok=True)

def garman_klass_volatility(df, window):
    """
    Rolling Garman Klass volatility estimator
    """
    #NOTE: by incorporating the full range of price movements, significantly reduces the variance in the estimator, captures intraday movement and overnight gaps
    #      computes average variance over window days 

    #NOTE: numpy here only to help with computation
    log_hl = np.log(df['High']/df['Low'])
    log_co = np.log(df['Close']/df['Open'])
    gk_var = 0.5 * log_hl**2 - (2 * np.log(2) - 1) * log_co**2
    
    #NOTE: rolling window is a method provided by the pandas library and goings through all the data in window number of intervals, it expects a pandas dataframe
    rolling_vol = np.sqrt(gk_var.rolling(window).mean())
    return rolling_vol


df = pd.read_csv(RAW_DATA_DIR / "oil_futures/oil_futures_daily.csv", parse_dates=["Date"])
df.set_index('Date', inplace=True) #allows dates to be read as a date time object and used as a index

df['vol_gk'] = garman_klass_volatility(df, 20)

print(df.tail())

