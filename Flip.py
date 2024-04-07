import os
import requests
import logging
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from transformers import pipeline
from web3 import Web3, HTTPProvider

# Improved logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NFTTrader:
    def __init__(self):
        self.api_key = os.getenv('OPENSEA_API_KEY')
        self.eth_node_url = os.getenv('ETH_NODE_URL')  # Infura or similar service URL
        self.wallet_address = os.getenv('WALLET_ADDRESS')
        self.wallet_private_key = os.getenv('WALLET_PRIVATE_KEY')
        self.headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        self.web3 = Web3(HTTPProvider(self.eth_node_url))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to Ethereum node.")

    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_analyzer(text)
            return result[0]['label'], result[0]['score']
        except Exception as e:
            logging.error(f"Sentiment analysis error: {e}")
            return None, None

    def get_nft_details(self, nft_contract_address, nft_token_id):
        url = f"https://api.opensea.io/api/v1/asset/{nft_contract_address}/{nft_token_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if 'asset' in data and 'last_sale' in data['asset']:
                current_price = data['asset']['last_sale']['total_price']
                description = data['asset']['description']
                sentiment_label, sentiment_score = self.analyze_sentiment(description)
                return current_price, sentiment_label, sentiment_score
            else:
                logging.error("Invalid data structure received from API.")
                return None, None, None
        except requests.RequestException as e:
            logging.error(f"Error retrieving NFT details: {e}")
            return None, None, None

    def fetch_historical_prices(self, nft_contract_address, nft_token_id):
        url = f"https://api.opensea.io/api/v1/asset/{nft_contract_address}/{nft_token_id}/events"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            prices = [float(event['total_price']) / 10**18 for event in data['asset_events'] if 'total_price' in event]
            return prices
        except requests.RequestException as e:
            logging.error(f"Error fetching historical prices: {e}")
            return []

    def forecast_price(self, historical_prices):
        if len(historical_prices) < 2:
            logging.warning("Insufficient data for forecasting.")
            return None

        X = np.arange(len(historical_prices)).reshape(-1, 1)
        y = np.array(historical_prices)
        model = RandomForestRegressor()

        tscv = TimeSeriesSplit(n_splits=5)
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            model.fit(X_train, y_train)

        next_price = model.predict([[len(historical_prices)]])
        return next_price[0]

    def buy_nft(self, nft_contract_address, nft_token_id, max_price):
        historical_prices = self.fetch_historical_prices(nft_contract_address, nft_token_id)
        forecasted_price = self.forecast_price(historical_prices)

        if forecasted_price is None:
            logging.error("Unable to forecast price. Transaction aborted.")
            return False

        if forecasted_price <= max_price:
            logging.info(f"Attempting to buy NFT at price: {forecasted_price} ETH")
            # Define the NFT contract ABI and create a contract object
            nft_contract_abi = 'YOUR_CONTRACT_ABI'  # Replace with actual ABI
            contract = self.web3.eth.contract(address=nft_contract_address, abi=nft_contract_abi)

            # Set up the transaction
            value_eth = self.web3.toWei(forecasted_price, 'ether')
            nonce = self.web3.eth.getTransactionCount(self.wallet_address)
            tx = contract.functions.transferFrom(self.wallet_address, nft_contract_address, nft_token_id).buildTransaction({
                'chainId': 1,  # Mainnet chain ID
                'gas': 200000,
                'gasPrice': self.web3.toWei('50', 'gwei'),
                'nonce': nonce,
                'value': value_eth
            })

            # Sign and send the transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.wallet_private_key)
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            logging.info(f"Transaction sent, TX Hash: {tx_hash.hex()}")
            return True
        else:
            logging.info("Forecasted price is higher than the max price. Transaction aborted.")
            return False

def main():
    nft_trader = NFTTrader()
    nft_contract_address = "NFT_CONTRACT_ADDRESS"
    nft_token_id = "NFT_TOKEN_ID"
    max_price = 1.0  # Example max price in ETH

    current_price, sentiment_label, sentiment_score = nft_trader.get_nft_details(nft_contract_address, nft_token_id)
    if current_price is not None and sentiment_label == "POSITIVE":
        logging.info(f"Current Price: {current_price}, Sentiment: {sentiment_label}({sentiment_score})")
        success = nft_trader.buy_nft(nft_contract_address, nft_token_id, max_price)
        if success:
            logging.info("NFT purchased successfully.")
        else:
            logging.info("NFT purchase failed or aborted.")
    else:
        logging.error("Failed to retrieve NFT details or negative sentiment.")

if __name__ == "__main__":
    main()
