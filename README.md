# GifGal-NFTtrader

GifGal-NFTtrader is a Python script designed to facilitate the analysis, forecasting, and trading of non-fungible tokens (NFTs) on the OpenSea platform. This README provides information on installation, usage, functionality, and a disclaimer.

## Prerequisites
- Python 3.x
- Required libraries: requests, logging, TextBlob, sklearn

## Installation
1. Clone or download the repository.
2. Install the required libraries using pip:
   ```
   pip install requests
   pip install textblob
   pip install scikit-learn
   ```

3. Replace `"YOUR_OPENSEA_API_KEY"`, `"YOUR_NFT_CONTRACT_ADDRESS"`, and `"YOUR_NFT_TOKEN_ID"` with appropriate values in the `main()` function.

## Usage
1. Run the script by executing the following command:
   ```
   python Flip.py
   ```

2. Check the logging output for information on NFT price, sentiment analysis, forecasted price, and trading actions.

## Functionality
- **analyze_sentiment(text):** Analyzes text sentiment using TextBlob.
- **forecast_price(historical_prices):** Predicts the next NFT price using historical data and a Random Forest Regressor model.
- **get_nft_details(nft_contract_address, nft_token_id):** Retrieves NFT details, including price and sentiment score.
- **buy_nft(nft_contract_address, nft_token_id, max_price):** Places a buy order for an NFT if the price is within the acceptable range.
- **fetch_historical_prices(nft_contract_address, nft_token_id):** Fetches historical NFT prices.

## Disclaimer
This script is provided for educational purposes only. Use it responsibly and at your own risk.
