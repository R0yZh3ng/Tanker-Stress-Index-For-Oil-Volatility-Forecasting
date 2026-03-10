import numpy as np
import pandas as pd

from utils.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

#processed data paths
PROCESSED_OIL_FUTURES_DIR = PROCESSED_DATA_DIR / "oil_futures"
PROCESSED_OIL_FUTURES_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_BDTI_DIR = PROCESSED_DATA_DIR / "bdti"
PROCESSED_BDTI_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_FINAL = PROCESSED_DATA_DIR / "final_concoction"
PROCESSED_FINAL.mkdir(parents=True, exist_ok=True)

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


oil_df = pd.read_csv(RAW_DATA_DIR / "oil_futures/oil_futures_daily.csv", parse_dates=["Date"])
oil_df.set_index('Date', inplace=True) #allows dates to be read as a date time object and used as a index

#NOTE: this adds a column using the function
oil_df['vol_gk'] = garman_klass_volatility(oil_df, 20)

oil_df.to_csv(PROCESSED_OIL_FUTURES_DIR / "oil_futures_daily_with_volgk.csv")

print(f"added vol_gk to oil_futures data {len(oil_df) - 20} rows of data (excluding the first 20 since we are using a rolling window of 20)")


#NOTE: the reason why the below is commented out is that it works but investing.com provided bad data, will have to work with what i have for now, so commenting this out to save resources

#def bdti_daily_range(df):
#    """
#    Daily percentage range calculation for bdti data
#    """
#    #NOTE: higher bdti range tells us that the tanker market stress spiked, using this to correlate to futures price volatility is more accurate
#
#    #NOTE: the blow code changes the columns to numbers instead and remove commas if neccesary
#
#    df["Price"] = pd.to_numeric(df["Price"].str.replace(",", ""), errors="coerce")
#    df["High"] = pd.to_numeric(df["High"].str.replace(",", ""), errors="coerce")
#    df["Low"] = pd.to_numeric(df["Low"].str.replace(",", ""), errors="coerce")
#    df["Open"] = pd.to_numeric(df["Open"].str.replace(",", ""), errors="coerce")
#    df["Change %"] = pd.to_numeric(df["Change %"].str.replace(",", ""), errors="coerce")
#
#
#    return (df['High'] - df['Low'])/df['Open']
#
#bdti_df = pd.read_csv(RAW_DATA_DIR / "bdti/Baltic_Dirty_Tanker_daily.csv", parse_dates=["Date"])
#bdti_df.set_index('Date', inplace=True)
#
#bdti_df['Range'] = bdti_daily_range(bdti_df)

bdti_df = pd.read_csv(RAW_DATA_DIR / "bdti/Baltic_Dirty_Tanker_daily.csv", parse_dates=["Date"])
bdti_df.set_index('Date', inplace=True)

bdti_df["decimal_change"] = (bdti_df["Change %"].str.strip("%").str.replace(",", "").astype(float))

#NOTE: create lagged days because market reaction to data is often delayed
bdti_df["lag_1_day"] = bdti_df["decimal_change"].shift(1)
bdti_df["lag_3_day"] = bdti_df["decimal_change"].shift(3)
bdti_df["lag_5_day"] = bdti_df["decimal_change"].shift(5)

bdti_df.to_csv(PROCESSED_BDTI_DIR / "bdti_with_daily_range.csv")

print(f"added daily percentage to bdti data of {len(bdti_df)} rows")
