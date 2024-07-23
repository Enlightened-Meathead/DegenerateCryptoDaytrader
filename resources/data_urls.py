# If you want to grab more Coinbase websocket accessible pricing data, just add the name you want to see in the user
# menu for selecting the asset as the dictionary key then the ticker symbol that Coinbase has in their public API.
# For investing.com RSI data, just add more url variables and add then to the asset_url_pair Data stream URLs for

# gathering price and RSI info PID 1057391 for the price,
btc_url = 'https://www.investing.com/crypto/bitcoin/technical'
eth_url = 'https://www.investing.com/crypto/ethereum/technical'
sol_url = 'https://www.investing.com/crypto/solana/technical'
xrp_url = 'https://www.investing.com/crypto/xrp/technical'
ada_url = 'https://www.investing.com/crypto/cardano/technical'
doge_url = 'https://www.investing.com/crypto/dogecoin/technical'
shiba_url = 'https://www.investing.com/crypto/shiba-inu/technical'
xmr_url = 'https://www.investing.com/crypto/monero/techinical'
hbar_url = 'https://www.investing.com/crypto/hedera/technical'

asset_ticker_pair = {'bitcoin': 'BTC', 'ethereum': 'ETH', 'solana': 'SOL', 'xrp': 'XRP', 'cardano': 'ADA',
                     'dogecoin': 'DOGE', 'shiba-inu': 'SHIB', 'monero': 'XMR', 'hedera': 'HBAR'
                     }
asset_url_pair = {'bitcoin': btc_url, 'ethereum': eth_url, 'solana': sol_url, 'xrp': xrp_url, 'cardano': ada_url,
                  'dogecoin': doge_url, 'shiba-inu': shiba_url, 'monero': xrp_url, 'hedera': hbar_url
                  }
