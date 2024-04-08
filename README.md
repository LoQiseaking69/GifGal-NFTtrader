# GifGal-NFTtrader
[![Build Status](https://github.com/LoQiseaking69/GifGal-NFTtrader/actions/workflows/main.yml/badge.svg)](https://github.com/LoQiseaking69/GifGal-NFTtrader/actions)
[![Coverage Status](https://coveralls.io/repos/github/LoQiseaking69/GifGal-NFTtrader/badge.svg?branch=main)](https://coveralls.io/github/LoQiseaking69/GifGal-NFTtrader?branch=main)
[![Maintainability](https://api.codeclimate.com/v1/badges/YourBadgeID/maintainability)](https://codeclimate.com/github/LoQiseaking69/GifGal-NFTtrader/maintainability)
[![License](https://img.shields.io/github/license/LoQiseaking69/GifGal-NFTtrader)](LICENSE)
GifGal-NFTtrader is a sophisticated Python script for automated trading of non-fungible tokens (NFTs) on Ethereum blockchain, particularly focusing on OpenSea platform transactions. This README guides you through installation, usage, functionalities, and includes a disclaimer.

![GifGal](https://github.com/LoQiseaking69/GifGal-NFTtrader/blob/main/IMG_8549.JPG)

## Prerequisites
- Python 3.x
- Required libraries: requests, logging, numpy, sklearn, transformers, web3

## Installation
1. Clone or download the repository.
2. Install the required libraries using pip:
   ```
   pip install requests numpy scikit-learn transformers web3
   ```

3. Obtain and set your OpenSea API key, Ethereum node URL, and Ethereum wallet details. Ensure these are stored securely, preferably as environment variables.

## Usage
1. Run the script using the following command:
   ```
   python Flip.py
   ```

2. Monitor the console for log information on sentiment analysis, price forecasting, and automated trading decisions.

## Functionality
- **analyze_sentiment(text):** Conducts sentiment analysis of NFT descriptions.
- **get_nft_details(nft_contract_address, nft_token_id):** Retrieves current NFT details including price and sentiment score.
- **fetch_historical_prices(nft_contract_address, nft_token_id):** Obtains historical price data of an NFT.
- **forecast_price(historical_prices):** Predicts future NFT price using a Random Forest Regressor model based on historical price data.
- **buy_nft(nft_contract_address, nft_token_id, max_price):** Executes a purchase of an NFT if predicted price is within a specified maximum limit.

## Disclaimer
This script is intended for educational and research purposes only. Use at your own risk. The creators are not responsible for any financial losses or legal implications arising from its use. Ensure you understand blockchain transactions, NFT trading, and the associated risks before use.
