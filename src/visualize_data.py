from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from utils.paths import PROJECT_ROOT, RAW_DATA_DIR, PROCESSED_DATA_DIR

FIGURES_DIR = PROJECT_ROOT / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(PROCESSED_DATA_DIR / "oil_futures/oil_futures_daily_with_volgk.csv", parse_dates=['Date'])

def plot_volatility(df):
    plt.figure()
    plt.plot(df['Date'], df['vol_gk'], linestyle='-', color='red')
    plt.xlabel("Dates")
    plt.ylabel("volatility_GK")
    plt.title("Volatility of oil_futures")
    plt.grid()
    plt.savefig(FIGURES_DIR / "volatility_GK.png")
    plt.close()

if __name__ == "__main__":
    plot_volatility(df)

