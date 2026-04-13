import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ================================
# SETTINGS
# ================================

DATA_FOLDER = "nifty50_data"

BENCHMARK = "NIFTYBEES.NS"

TOP_N = 5

INITIAL_CAPITAL = 50000

# ================================
# LOAD DATA
# ================================

def load_stock_data():

    stock_data = {}

    for file in os.listdir(DATA_FOLDER):

        if not file.endswith(".csv"):
            continue

        ticker = file.replace(".csv", "")

        file_path = os.path.join(DATA_FOLDER, file)

        try:

            df = pd.read_csv(
                file_path,
                parse_dates=["Date"]
            )

            df.set_index("Date", inplace=True)

            # Convert to numeric (fix string issue)
            df["Adj Close"] = pd.to_numeric(
                df["Adj Close"],
                errors="coerce"
            )

            df = df.dropna()

            stock_data[ticker] = df["Adj Close"]

        except Exception as e:

            print(f"Skipping {ticker}: {e}")

    return stock_data

stock_data = load_stock_data()

# ================================
# CREATE MONTH-END DATA
# ================================

monthly_prices = pd.DataFrame()

for ticker, series in stock_data.items():

    monthly_prices[ticker] = series.resample("BME").last()

# Keep partial monthly data across stocks.
# Only drop tickers that never have a monthly price.
monthly_prices = monthly_prices.dropna(axis=1, how="all")

# ================================
# MONTHLY RETURNS
# ================================

monthly_returns = monthly_prices.pct_change()
monthly_returns = monthly_returns.dropna(how="all")

if len(monthly_returns) < 2:
    raise ValueError(
        "Not enough monthly history to run the backtest. "
        f"Found only {len(monthly_returns)} monthly return period(s). "
        "Download more history or use a shorter rebalance frequency."
    )

# Benchmark returns
benchmark_returns = monthly_returns[BENCHMARK]

# ================================
# RELATIVE STRENGTH
# ================================

relative_strength = monthly_returns.sub(
    benchmark_returns,
    axis=0
)

# ================================
# BACKTEST
# ================================

portfolio_value = INITIAL_CAPITAL
portfolio_history = []

dates = monthly_returns.index

for i in range(len(dates) - 1):

    current_date = dates[i]
    next_date = dates[i + 1]

    # Get RS values
    rs_today = relative_strength.loc[current_date]

    # Remove benchmark
    rs_today = rs_today.drop(
        labels=[BENCHMARK],
        errors="ignore"
    )

    # Remove NaNs
    rs_today = rs_today.dropna()

    # Skip if not enough stocks
    if len(rs_today) < TOP_N:
        continue

    # Select top N stocks
    top_stocks = rs_today.nlargest(TOP_N).index

    # Get next month returns
    next_returns = monthly_returns.loc[next_date]

    selected_returns = next_returns[top_stocks]

    # Remove NaNs
    selected_returns = selected_returns.dropna()

    if len(selected_returns) == 0:
        continue

    # Equal weight return
    portfolio_return = selected_returns.mean()

    portfolio_value *= (1 + portfolio_return)

    portfolio_history.append({
        "Date": next_date,
        "Portfolio_Value": portfolio_value,
        "Stocks": ",".join(top_stocks)
    })


# Convert to DataFrame
portfolio_df = pd.DataFrame(portfolio_history)

# Critical safety check
if portfolio_df.empty:

    raise ValueError(
        "Portfolio dataframe is empty.\n"
        "Likely causes:\n"
        "- Benchmark missing\n"
        "- Too many NaNs\n"
        "- No overlapping stock data"
    )

portfolio_df.set_index("Date", inplace=True)

# ================================
# BENCHMARK PERFORMANCE
# ================================

benchmark_value = INITIAL_CAPITAL

benchmark_history = []

for i in range(1, len(dates)):

    ret = benchmark_returns.iloc[i]

    benchmark_value *= (1 + ret)

    benchmark_history.append({
        "Date": dates[i],
        "Benchmark_Value": benchmark_value
    })

benchmark_df = pd.DataFrame(benchmark_history)

benchmark_df.set_index("Date", inplace=True)

# ================================
# MERGE RESULTS
# ================================

results = portfolio_df.join(
    benchmark_df,
    how="inner"
)

# ================================
# SAVE RESULTS
# ================================

results.to_csv("momentum_backtest_results.csv")

print("Backtest results saved.")

# ================================
# PERFORMANCE METRICS
# ================================

def compute_metrics(series):

    returns = series.pct_change().dropna()

    cagr = (
        (series.iloc[-1] / series.iloc[0])
        ** (12 / len(series))
        - 1
    )

    volatility = returns.std() * np.sqrt(12)

    sharpe = returns.mean() / returns.std() * np.sqrt(12)

    max_dd = (
        (series / series.cummax()) - 1
    ).min()

    return {
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Max Drawdown": max_dd
    }

portfolio_metrics = compute_metrics(
    results["Portfolio_Value"]
)

benchmark_metrics = compute_metrics(
    results["Benchmark_Value"]
)

print("\nPortfolio Metrics:")
print(portfolio_metrics)

print("\nBenchmark Metrics:")
print(benchmark_metrics)

# ================================
# PLOT EQUITY CURVE
# ================================

plt.figure(figsize=(12,6))

plt.plot(
    results.index,
    results["Portfolio_Value"],
    label="Momentum Portfolio"
)

plt.plot(
    results.index,
    results["Benchmark_Value"],
    label="Benchmark"
)

plt.legend()

plt.title("Momentum Strategy vs Benchmark")

plt.xlabel("Date")

plt.ylabel("Portfolio Value")

plt.grid()

plt.show()