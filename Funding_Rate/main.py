"""
An example of fetching funding rate history
"""
from funding_rate_arbitrage.frarb import FundingRateArbitrage
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    fr = FundingRateArbitrage()

    binance_time, binance_rate = fr.fetch_funding_rate_history(exchange="binance", symbol="MINA/USDT:USDT")
    okx_time, okx_rate = fr.fetch_funding_rate_history(exchange="okx", symbol="MINA/USDT:USDT")


    binance_df = pd.DataFrame({"timestamp": binance_time, "binance_rate": binance_rate})
    okx_df = pd.DataFrame({"timestamp": okx_time, "okx_rate": okx_rate})

    # keep only common timestamps
    merged_df = pd.merge(binance_df, okx_df, on="timestamp", how="inner")


    plt.figure(figsize=(10, 5))
    plt.plot(merged_df["timestamp"], merged_df["binance_rate"], label="Binance funding rate")
    plt.plot(merged_df["timestamp"], merged_df["okx_rate"], label="OKX funding rate")


    plt.title("Funding Rate History for MINA/USDT")
    plt.xlabel("Timestamp")
    plt.ylabel("Funding Rate %")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.show()
