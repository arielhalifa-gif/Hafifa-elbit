from pathlib import Path
from dotenv import load_dotenv
import os
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# -------------------------
# SETUP
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv()

# -------------------------
# CONFIG
# -------------------------
STOCKS = {
    "Bitcoin": "BTC-USD",
    "Google": "GOOGL",
    "Amazon": "AMZN"
}

ENV_FILES = {
    "Bitcoin": "BITCOIN_DATES",
    "Google": "GOOGLE_DATES",
    "Amazon": "AMAZON_DATES"
}

output_file = os.getenv("DESTINATION_FILE")

if not output_file:
    raise ValueError("Missing DESTINATION_FILE")

# -------------------------
# LOAD STOCK DATA
# -------------------------
data = {}

for name, ticker in STOCKS.items():
    df = yf.download(ticker, interval="1h", period="730d")
    df.index = df.index.tz_localize(None)

    if df.empty:
        raise ValueError(f"No data returned for {name}")

    data[name] = df["Close"].squeeze()

# -------------------------
# LOAD INPUT HOURS
# -------------------------
hours_data = {}

for name in STOCKS:
    env_var = ENV_FILES[name]
    relative_path = os.getenv(env_var)

    if not relative_path:
        raise ValueError(f"Missing env var: {env_var}")

    file_path = BASE_DIR / relative_path

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as f:
        hours = [
            pd.to_datetime(line.strip()).floor("h")
            for line in f
            if line.strip()
        ]

    hours_data[name] = hours

# -------------------------
# CALCULATION FUNCTION
# -------------------------
def calculate(stock_name, i):
    series = data[stock_name]
    hours = hours_data[stock_name]

    if i == 0:
        return None

    p_now = series.asof(hours[i])
    p_prev = series.asof(hours[i - 1])

    if pd.isna(p_now) or pd.isna(p_prev):
        return None

    pct_change = (p_now - p_prev) / p_prev * 100

    return {
        "hour": hours[i],
        "stock_type": stock_name,
        "percentage_change": round(float(pct_change), 4)
    }

# -------------------------
# THREAD EXECUTION
# -------------------------
tasks = [
    (stock, i)
    for stock in STOCKS
    for i in range(1, len(hours_data[stock]))
]

with ThreadPoolExecutor() as executor:
    results = list(executor.map(lambda x: calculate(*x), tasks))

results = [r for r in results if r is not None]

# -------------------------
# SAVE OUTPUT
# -------------------------
df = pd.DataFrame(results)

if df.empty:
    raise ValueError("No valid results generated. Check input dates vs stock data.")

df = df.sort_values(["stock_type", "hour"])
df.to_csv(output_file, index=False)

print("Done → CSV created successfully")