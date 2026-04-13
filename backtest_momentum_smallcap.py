import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

DATA_FOLDER = "smallcap_data"
BENCHMARK = "HDFCSML250.NS"
TOP_N = 5
INITIAL_CAPITAL = 50000

def load_stock_data():
    stock_data = {}
    for file in os.listdir(DATA_FOLDER):
        if not file.endswith(".csv"):
            continue
        ticker = file.replace(".csv", "")
        file_path = os.path.join(DATA_FOLDER, file)
        try:
            df = pd.read_csv(file_path, parse_dates=["Date"])
            df.set_index("Date", inplace=True)
            df["Adj Close"] = pd.to_numeric(df["Adj Close"], errors="coerce")
            df = df.dropna()
            stock_data[ticker] = df["Adj Close"]
        except Exception as e:
            print(f"Skipping {ticker}: {e}")
    return stock_data

stock_data = load_stock_data()

monthly_prices = pd.DataFrame()
for ticker, series in stock_data.items():
    monthly_prices[ticker] = series.resample("BME").last()
monthly_prices = monthly_prices.dropna(axis=1, how="all")

monthly_returns = monthly_prices.pct_change()
monthly_returns = monthly_returns.dropna(how="all")

if len(monthly_returns) < 2:
    raise ValueError(
        "Not enough monthly history to run the backtest. "
        f"Found only {len(monthly_returns)} monthly return period(s). "
        "Download more history or use a shorter rebalance frequency."
    )

benchmark_returns = monthly_returns[BENCHMARK]
relative_strength = monthly_returns.sub(benchmark_returns, axis=0)

portfolio_value = INITIAL_CAPITAL
portfolio_history = []
dates = monthly_returns.index

for i in range(len(dates) - 1):
    current_date = dates[i]
    next_date = dates[i + 1]
    rs_today = relative_strength.loc[current_date]
    rs_today = rs_today.drop(labels=[BENCHMARK], errors="ignore")
    rs_today = rs_today.dropna()
    if len(rs_today) < TOP_N:
        continue
    top_stocks = rs_today.nlargest(TOP_N).index
    next_returns = monthly_returns.loc[next_date]
    selected_returns = next_returns[top_stocks]
    selected_returns = selected_returns.dropna()
    if len(selected_returns) == 0:
        continue
    portfolio_return = selected_returns.mean()
    portfolio_value *= (1 + portfolio_return)
    portfolio_history.append({
        "Date": next_date,
        "Portfolio_Value": portfolio_value,
        "Stocks": ",".join(top_stocks)
    })

portfolio_df = pd.DataFrame(portfolio_history)

if portfolio_df.empty:
    raise ValueError(
        "Portfolio dataframe is empty.\n"
        "Likely causes:\n"
        "- Benchmark missing\n"
        "- Too many NaNs\n"
        "- No overlapping stock data"
    )

portfolio_df.set_index("Date", inplace=True)

benchmark_value = INITIAL_CAPITAL
benchmark_history = []
for i in range(1, len(dates)):
    ret = benchmark_returns.iloc[i]
    benchmark_value *= (1 + ret)
    benchmark_history.append({"Date": dates[i], "Benchmark_Value": benchmark_value})

benchmark_df = pd.DataFrame(benchmark_history)
benchmark_df.set_index("Date", inplace=True)

results = portfolio_df.join(benchmark_df, how="inner")
results.to_csv("momentum_backtest_results_smallcap.csv")
print("Backtest results saved.")

def compute_metrics(series):
    returns = series.pct_change().dropna()
    cagr = ((series.iloc[-1] / series.iloc[0]) ** (12 / len(series)) - 1)
    volatility = returns.std() * np.sqrt(12)
    sharpe = returns.mean() / returns.std() * np.sqrt(12)
    max_dd = ((series / series.cummax()) - 1).min()
    return {"CAGR": cagr, "Volatility": volatility, "Sharpe": sharpe, "Max Drawdown": max_dd}

portfolio_metrics = compute_metrics(results["Portfolio_Value"])
benchmark_metrics = compute_metrics(results["Benchmark_Value"])
print("\nPortfolio Metrics:")
print(portfolio_metrics)
print("\nBenchmark Metrics:")
print(benchmark_metrics)

plt.figure(figsize=(12,6))
plt.plot(results.index, results["Portfolio_Value"], label="Momentum Portfolio")
plt.plot(results.index, results["Benchmark_Value"], label="Benchmark")
plt.legend()
plt.title("Momentum Strategy vs Benchmark (Smallcap)")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.grid()
plt.show()
