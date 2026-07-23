import pandas as pd
import numpy as np

df = pd.read_csv("crypto_data.csv")
print(df.head())

print("percentage below")
print(df["price_change_percentage_24h"])

#fix NAN value
df["price_change_percentage_24h"] = pd.to_numeric(df["price_change_percentage_24h"], errors="coerce")
df["price_change_percentage_24h"] = df["price_change_percentage_24h"].fillna(0)

#Convert columns into Numpy Arrays
prices= df["current_price"].to_numpy()
percentage_change = df["price_change_percentage_24h"].to_numpy()
market_caps = df["market_cap"].to_numpy()

print("\nNumpy Arrays created:")
print("\nPrices",prices)
print("\nPercentage change", percentage_change)
print("\nMarket Caps", market_caps)

#Calculate daily returns - foundation of financial analysis
daily_returns = percentage_change / 100
print("\nDaily returns:")
print(daily_returns)

#Calculate Volatility - how wild teh market is, how risky or stable the coins are
volatility = np.std(daily_returns)
print("\nMarket Volatility (std of returns):", volatility)

#Normalize values - min max scaling- helps to comapre the coins fairly even if their prices differ massively
normalized_prices = (prices - prices.min()) / (prices.max() - prices.min())
print("\nNormalized prices:")
print(normalized_prices)

#Build a Numpy analysis function - used to detect breakouts, crashes, high-risk coins
def find_extreme_returns(df, threshold):
    percentage = df["price_change_percentage_24h"].to_numpy()
    mask = np.abs(percentage) > threshold
    return df[mask]

extreme = find_extreme_returns(df,5)
print("\n Coins with >5% movement:")
print(extreme)

#Calculate Risk Score
risk_score = np.abs(percentage_change) / np.sqrt(market_caps)
df["risk_score"] = risk_score

print("\nRisk scores added:")
print(df[["name", "risk_score"]])