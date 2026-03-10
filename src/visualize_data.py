from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from utils.paths import PROJECT_ROOT, RAW_DATA_DIR, PROCESSED_DATA_DIR

FIGURES_DIR = PROJECT_ROOT / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)



def plot_volatility(df):
    plt.figure()
    plt.plot(df['Date'], df['vol_gk'], linestyle='-', color='red')
    plt.xlabel("Dates")
    plt.ylabel("volatility_GK")
    plt.title("Volatility of oil_futures")
    plt.grid()
    plt.savefig(FIGURES_DIR / "volatility_GK.png")
    plt.close()

def plot_change(df):
    plt.figure()
    plt.plot(df['Date'], df['decimal_change'], linestyle='-', color='red')
    plt.plot(df['Date'], df['lag_1_day'], linestyle='-', color='blue')
    plt.plot(df['Date'], df['lag_3_day'], linestyle='-', color='green')
    plt.plot(df['Date'], df['lag_5_day'], linestyle='-', color='yellow')
    plt.title("daily bdti")
    plt.xlabel("Dates")
    plt.ylabel("Percentage change")
    plt.grid()
    plt.savefig(FIGURES_DIR / "bdti.png")
    plt.close()


oil_df = pd.read_csv(PROCESSED_DATA_DIR / "oil_futures/oil_futures_daily_with_volgk.csv", parse_dates=['Date'])
bdti_df = pd.read_csv(PROCESSED_DATA_DIR / "bdti/bdti_with_change_and_lag.csv", parse_dates=['Date'])


if __name__ == "__main__":
    plot_volatility(oil_df)
    plot_change(bdti_df)

