import pandas as pd
import json

#Load clean json
with open("clean_crypto_data.json","r") as f:
    data = json.load(f)

#Convert to data frame
df = pd.DataFrame(data)

print(df.head())

print("\nColumns:")
print(df.columns)

print("\nBasic Info:")
print(df.info())

print("\n Summary Statistics:")
print(df.describe())

#Sort Data
print("\nTop Gainers (24h %):")
print(df.sort_values("price_change_percentage_24h", ascending=False).head(5))

print("\nTop Losers (24h %):")
print(df.sort_values("price_change_percentage_24h").head(5))

#Filter Data
expensive = df[df["current_price"] > 5000]
print("\nCoins above $5000:")
print(expensive)

high_volume = df[df["total_volume"] > 10_000_000_000]
print("\nHigh volume coins:")
print(high_volume)

big_drops = df[df["price_change_percentage_24h"]< -5]
print("\nCoins dropped more than 5%:")
print(big_drops)

#Add new calculated columns - column- market cap in billions and price change in USD per $1000 invested
df["market_cap_billion"] = df["market_cap"] / 1_000_000_000

df["usd_change_per_1000"] = df["price_change_percentage_24h"] / 100 * 1000

print("\nUpdated data frame with new columns:")
print(df.head())

#save data frame as csv file
df.to_csv("crypto_data.csv", index=False)
print("\n CSV is saved as crypto_data.csv")