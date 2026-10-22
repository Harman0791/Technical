import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("crypto_data.csv")
sns.set_theme(style="whitegrid")

#Bar chart: current prices - a simple bar chart of all crypto prices
plt.figure(figsize=(12,6))
sns.barplot(x="name",y="current_price", data=df)
plt.xticks(rotation= 45)
plt.title("Crypto Prices")
plt.tight_layout()
plt.savefig("screenshots/current_price_chart.png")
plt.show()


#Bar Chart: market caps - shows size and stability of each coin
plt.figure(figsize=(12,6))
sns.barplot(x="name", y="market_cap", data=df)
plt.xticks(rotation= 45)
plt.title("Market Caps")
plt.tight_layout()
plt.savefig("screenshots/market_cap_chart.png")
plt.show()

#scatter plot- price versus market cap - show relationship between price an dmarket size
plt.figure(figsize=(10,6))
sns.scatterplot(x="market_cap", y="current_price", hue="name", data=df, s=200)
plt.title("Price vs Market Cap")
plt.tight_layout()
plt.show()

#Bar chart 24h percentage change - shows top gainers and losers visually
plt.figure(figsize=(12,6))
sns.barplot(x="name",y="price_change_percentage_24h",data=df)
plt.xticks(rotation=45)
plt.title("24h percentage change")
plt.tight_layout()
plt.show()

#Heat Map: correlation between metrics - show relationship b/w price, marketcap, volume, returns, risk score
numeric_df = df.select_dtypes(include=['float64','int64'])
plt.figure(figsize=(10,6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation HeatMap")
plt.tight_layout()
plt.savefig("screenshots/heat_map.png")
plt.show()

#Line chart: Sorted prices - shows a clean price distribution
sorted_df = df.sort_values("current_price")

plt.figure(figsize=(12,6))
plt.plot(sorted_df["name"], sorted_df["current_price"], marker="o")
plt.xticks(rotation=45)
plt.title("Sorted crypto prices")
plt.tight_layout()
plt.show()