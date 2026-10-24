import requests
import json

#class
class CryptoDataFetcher:
    def __init__(self,vs_currency="usd", per_page=10):
        self.url="https://api.coingecko.com/api/v3/coins/markets"
        self.params = {
            "vs_currency":vs_currency,
            "order":"market_cap_desc",
            "per_page":per_page,
            "page":1,
            "sparkline":False
        }
    
    def fetch_data(self):
        response = requests.get(self.url,params=self.params)
        data = response.json()
        return data
    
    def clean_data(self, raw_data):
        clean_list =[]
        for coin in raw_data:
            entry ={
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "current_price": coin.get("current_price"),
                "market_cap": coin.get("market_cap"),
                "price_change_24h": coin.get("price_change_24h"),
                "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
                "total_volume": coin.get("total_volume")
            }
            clean_list.append(entry)
        return(clean_list)
    
    def save_data(self,data, filename):
        with open(filename,"w") as f:
            json.dump(data,f, indent=4)
    
    def run(self):
        raw = self.fetch_data()
        clean = self.clean_data(raw)
        self.save_data(clean,"clean_crypto_data.json")
        return clean

