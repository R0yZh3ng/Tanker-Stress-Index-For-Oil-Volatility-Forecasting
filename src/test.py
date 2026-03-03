import pandas as pd
import glob
import os

RAW_FLARE_DATA_DIR = "/home/bokchoy/projects/Flare-Stress-Index-For-Oil-Volatility-Forecasting/data/raw/flares"
flare_files = sorted(glob.glob(os.path.join(RAW_FLARE_DATA_DIR, "*_flare_list.csv")))

# Check columns for the first file
df = pd.read_csv(flare_files[0])
print(df.columns)
