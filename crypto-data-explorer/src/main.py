from crypto_fetcher import CryptoDataFetcher
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def run_pipeline():
    print("Fetching fresh data...")
    fetcher = CryptoDataFetcher()
    clean_data = fetcher.run()

    print("\n Loading into pandas...")
    df = pd.DataFrame(clean_data)
    
    #fix NAN value
    df["price_change_percentage_24h"] = pd.to_numeric(df["price_change_percentage_24h"], errors="coerce")
    df["price_change_percentage_24h"] = df["price_change_percentage_24h"].fillna(0)


    print("\n Saving csv...")
    df.to_csv("crypto_data.csv", index= False)

    print("\n Converting to Numpy arrays...")
    prices = df["current_price"].to_numpy()
    percentage_change = df["price_change_percentage_24h"]. to_numpy()

    daily_returns = percentage_change / 100
    volatility = np.std(daily_returns)

    print("\nPipeline Complete")
    print("Volatility", volatility)

    return df, daily_returns, volatility

# Add a somple menu system
def show_menu():
    print("\n=== Crypto Data Explorer ===")
    print("\n1. Run full Pipeline")
    print("\n2. Show top gainers")
    print("\n3. Show top losers")
    print("\n4. Show Visualizations")
    print("\n5. Exit")

#Add menu actions
def main():
    df = None
    daily_returns = None
    volatility = None

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            df, daily_returns, volatility = run_pipeline()

        elif choice == "2":
            if df is None:
                print("Run Pipeline First!")
            else:
                print(df.sort_values("price_change_percentage_24h", ascending= False).head())
        
        elif choice == "3":
            if df is None:
                print("Run Pipeline First!")
            else:
                print(df.sort_values("price_change_percentage_24h").head())
        elif choice == "4":
            if df is None:
                print("Run Pipeline First!")
            else:
                sns.barplot(x="name", y="current_price", data = df)
                plt.xticks(rotation=45)
                plt.show()
        
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()



