import time

import scan_protocols as scp


# Basic Buy Function: Selects the market pair, gets value to buy at, calls the scan function to see what the price is,
# then once the price signal is reached, buys the asset
def basic_buy_scan(asset, buy_price, sleep_duration):
    # If the price of the asset is met, call the buy asset function
    buy_signal = False
    while not buy_signal:
        if float(buy_price) <= float(scp.current_price_scan()):
            # Initiate buy function for the asset named
            print(f"{asset} Bought due to basic buy")
            buy_signal = True
            return buy_signal
        else:
            time.sleep(sleep_duration)


# Revival buy function: if an asset is sold due to a stop loss limit initiating the sell, buy back the asset at the
# price it was sold at by the stop loss. Actually, the above can do that just fine, just need to link the buy price
# to the stop loss limit last sell price

# RSI buy function: Buy the asset when a certain user defined RSI is hit, the general recommended RSI to buy at is 30
def rsi_buy_scan(asset, time_span, rsi_buy_number,  rsi_drop_limit, wait_period, sleep_duration):
    # If the RSI number is met, initiate a buy protocol once the asset goes back above the rsi number for a set period
    buy_signal = False
    while not buy_signal:
        # If the RSI dips below the set number, start the wait period to make sure it's not going to dip way lower
        if float(scp.rsi_scan(asset, time_span)) <= rsi_buy_number:
            time.sleep(scp.time_to_seconds(wait_period))
            # If the timer expires and the rsi_drop limit has not been reacher, buy the asset
            if float(scp.rsi_scan(asset, time_span)) >= rsi_drop_limit:
                buy_signal = True
                print("Bought due to wait period expiring and drop limit not being hit")
                return buy_signal
                # Initiate buy Order
            else:
                print("slept due to RSI below the drop limit")
        else:
            time.sleep(sleep_duration)
