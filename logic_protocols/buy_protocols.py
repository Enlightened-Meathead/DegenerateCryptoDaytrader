# Basic Buy Function: Selects the market pair, gets value to buy at, calls the scan function to see what the price is,
# then once the price signal is reached, buys the asset
def basic_buy(asset, buy_price):
    # If the price of the asset is met, call the buy asset function
