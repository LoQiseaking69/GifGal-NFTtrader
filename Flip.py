import requests
import logging
from textblob import TextBlob
from sklearn.ensemble import RandomForestRegressor
import numpy as np

logging.basicConfig(level=logging.INFO)

class NFTTrader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    def forecast_price(self, historical_prices):
        X_train = np.arange(len(historical_prices)).reshape(-1, 1)
        y_train = historical_prices

        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        next_price = model.predict([[len(historical_prices)]])
        return next_price

    def get_nft_details(self, nft_contract_address, nft_token_id):
        url = f"https://api.opensea.io/api/v1/asset/{nft_contract_address}/{nft_token_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'asset' in data:
                current_price = data['asset']['last_sale']['total_price']
                description = data['asset']['description']
                sentiment_score = self.analyze_sentiment(description)
                return current_price, sentiment_score
        except requests.RequestException as e:
            logging.error(f"Error retrieving NFT details: {e}")
        return None, None

    def buy_nft(self, nft_contract_address, nft_token_id, max_price):
        url = f"https://api.opensea.io/api/v1/orders"
        payload = {
            "asset_contract_address": nft_contract_address,
            "token_id": nft_token_id,
            "side": 0,  # 0 for buy, 1 for sell
            "order_by": "created_date",
            "order_direction": "desc",
            "limit": 1
        }
        try:
            response = requests.get(url, headers=self.headers, params=payload)
            response.raise_for_status()
            data = response.json()
            if data.get('orders'):
                order = data['orders'][0]
                price = float(order['current_price']) / 1000000000000000000  # Convert from wei to ETH
                if price <= max_price:
                    # Place buy order
                    buy_url = "https://api.opensea.io/wyvern/v1/orders"
                    buy_payload = {
                        "side": 0,
                        "sale_kind": 0,
                        "asset": {
                            "token_id": nft_token_id,
                            "asset_contract_address": nft_contract_address,
                            "schema_name": "ERC721"
                        },
                        "payment_token_contract_address": "0x0000000000000000000000000000000000000000",  # ETH
                        "quantity": 1,
                        "maker": order['maker'],
                        "taker": "",  # Your address
                        "exchange": "opensea",
                        "base_price": order['current_price'],
                        "extra": 0,
                        "salt": order['salt'],
                        "fee_recipient": order['fee_recipient']
                    }
                    buy_response = requests.post(buy_url, headers=self.headers, json=buy_payload)
                    buy_response.raise_for_status()
                    return True
        except requests.RequestException as e:
            logging.error(f"Error buying NFT: {e}")
        return False
    
    def fetch_historical_prices(self, nft_contract_address, nft_token_id):
        url = f"https://api.opensea.io/api/v1/asset/{nft_contract_address}/{nft_token_id}/events"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            prices = []
            for event in data['asset_events']:
                if 'total_price' in event and 'payment_token' in event and event['payment_token']['symbol'] == 'ETH':
                    price_eth = float(event['total_price']) / 10**event['payment_token']['decimals']
                    prices.append(price_eth)
            return prices
        except requests.RequestException as e:
            logging.error(f"Error fetching historical prices: {e}")
        return []

def main():
    try:
        api_key = "YOUR_OPENSEA_API_KEY"
        nft_contract_address = "YOUR_NFT_CONTRACT_ADDRESS"
        nft_token_id = "YOUR_NFT_TOKEN_ID"
        max_price = 1.0
        
        nft_trader = NFTTrader(api_key)

        current_price, sentiment_score = nft_trader.get_nft_details(nft_contract_address, nft_token_id)

        if current_price is not None and sentiment_score is not None:
            logging.info(f"Current price of NFT {nft_token_id}: {current_price} ETH")
            logging.info(f"Sentiment score: {sentiment_score}")

            # Fetch real-time historical prices
            historical_prices = nft_trader.fetch_historical_prices(nft_contract_address, nft_token_id)

            if historical_prices:
                next_price = nft_trader.forecast_price(historical_prices)
                logging.info(f"Forecasted next price: {next_price}")

                if current_price <= max_price:
                    logging.info("Current price is within the acceptable range.")
                    buy_success = nft_trader.buy_nft(nft_contract_address, nft_token_id, max_price)
                    if buy_success:
                        logging.info("NFT bought successfully!")
                else:
                    logging.info("Current price is above the acceptable range. Waiting for price drop...")
            else:
                logging.error("Failed to fetch historical prices.")
        else:
            logging.error("Failed to retrieve NFT details.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
