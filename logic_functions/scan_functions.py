## Scans that repeatedly look for the desired outcome and returns the value based on the asset given
import time
import websockets
import json
import re
from selenium import webdriver

from resources import data_urls

# As of this comment, the coinbase public websocket seemingly only supports data on the cryptos they directly sell, so
# monero is currently not supported :'( will definitely add in the future...
asset_ticker_pair = {'bitcoin': 'BTC', 'ethereum': 'ETH', 'solana': 'SOL', 'xrp': 'XRP', 'cardano': 'ADA',
                     'dogecoin': 'DOGE', 'shiba-inu': 'SHIB', 'monero': 'XMR', 'hedera': 'HBAR'
                     }


def time_to_seconds(time_string):
    # Splits the hh:mm:ss format into seconds
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


async def connect_websocket():
    uri = "wss://ws-feed.exchange.coinbase.com"
    websocket = await websockets.connect(uri)
    return websocket


"""
 Asynchronous websocket based connection through coinbase that returns the price of the given ticker pair every 5 
 seconds. If you pass a websocket connection, it will keep scanning until the call ends the function, else it will 
 scan once
"""


async def current_price_scan(asset, websocket=None):
    # If the program just needs to scan the price once, open the connection within this function
    one_scan = False
    if websocket is None:
        one_scan = True
        websocket = await connect_websocket()
    # Subscribe to the websocket for the asset passed by the function call
    price_pair = asset_ticker_pair[asset] + '-USD'
    subscribe_message = json.dumps({
        "type": "subscribe",
        "product_ids": [price_pair],
        "channels": ["ticker_batch"]
    })
    await websocket.send(subscribe_message)
    # Return the price until the function that calls this function ends or close after one price grab if one time scan
    while True:
        try:
            response = await websocket.recv()
            json_response = json.loads(response)
            # Check if message is a ticker message then parse the price
            if 'type' in json_response and json_response['type'] == 'ticker' and 'price' in json_response:
                current_price = json_response['price']
                if one_scan:
                    await websocket.close()
                return float(current_price)
        except websockets.exceptions.ConnectionClosed:
            if not one_scan:
                print("Websocket connection closed unexpectedly. Attempting to reconnect...")
                websocket = await connect_websocket()
                await websocket.send(subscribe_message)


# Calculate the difference in percentage from the price bought to the current value of the asset
async def current_percent_difference(asset, bought_price, websocket):
    try:
        current_price = await current_price_scan(asset, websocket)
        percent_difference = ((float(current_price) / float(bought_price)) - 1) * 100
        return percent_difference
    except Exception as e:
        print(f"Error in current_percent_difference: {e}")


# Basic Buy Function: Selects the market pair, gets value to buy at, calls the scan function to see what the price is,
# then once the price signal is reached, signals to buy the asset
async def basic_buy_scan(asset, buy_price):
    # If the price of the asset is met, call the buy asset function
    websocket = await connect_websocket()
    try:
        while True:
            current_price = await current_price_scan(asset, websocket)
            if float(buy_price) >= float(current_price):
                # Initiate buy function for the asset named
                print(f"{asset} buy signal due to basic buy scan")
                await websocket.close()
                return True
    except Exception as e:
        print(f"Error in basic_buy_scan: {e}")


# RSI buy scan : returns the current RSI for the asset for the user defined span of time and based on input signal to
# buy. For now, just start with hourly RSI calculation to estimate RSI for the past 14 hours, experiment with time
# intervals later.

def rsi_buy_scan(asset, rsi_buy_number, rsi_drop_limit, rsi_wait_period):
    # Set the Firefox browser to headless, try later
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    # Launch firefox
    driver = webdriver.Firefox()
    # In the firefox browser, go to the desired asset URL
    driver.get(data_urls.asset_url_pair.get(asset))
    # On that page, find all the technical indicator rows in a table Iterate over every technical indicator,
    # and return the RSI (Or whatever other technical indicator you want to return)
    try:
        buy_signal = False
        while True:
            rows = driver.find_elements("css selector", "tr.datatable_row__Hk3IV")
            for row in rows:
                # Check for RSI
                if re.search(r"^RSI\(14\)", row.text):
                    # Make the row text only the RSI, then somehow return the RSI without exiting the function
                    rsi = float(re.search(r"\s(\d+\.\d+)\s", row.text).group(1).strip())
                    # In the future save the current row.text then only make it reference that one row once it's found
                    # to be more efficient
                    print(f"Current {asset} RSI: {rsi}")
                    if rsi <= rsi_buy_number:
                        # If the buy signal hasn't been activated, activate and start the wait period.
                        if not buy_signal:
                            buy_signal = True
                        # If the timer expires and the rsi_drop limit has not been reached, buy the asset
                        elif rsi >= rsi_drop_limit:
                            buy_signal = True
                            print(f"{asset} buy signal due to wait period expiring and drop limit not being hit")
                            return buy_signal
                            # Initiate buy Order
                        else:
                            buy_signal = False
                            print("slept due to RSI below the drop limit")
            # If buy signal is false, scan every 60 seconds, but if buy signal is True, then scan for the wait period
            if not buy_signal:
                time.sleep(20)
            elif buy_signal:
                time.sleep(time_to_seconds(rsi_wait_period))
    except Exception as e:
        print(f"Error in rsi_buy_scan: {e}")
    finally:
        driver.quit()


'''
 Basic sell scan: given the users desired percentage gain from the bought price, send true once that percentage is met
 Bought price is the price you bought it originally, percent wanted is the float number percentage, ie 5.5% is just
 5.5, and percent loss limit is the whole float number percentage started with a  negative value, ie 2.2% max loss 
 before you sell is -2.2
'''


async def basic_sell_scan(asset, bought_price, percent_wanted, percent_loss_limit):
    # While the percent wanted is not equal to the current potential profit
    websocket = await connect_websocket()
    while True:
        # Calculates the potential profit or loss percentage
        percent_difference = await current_percent_difference(asset, bought_price, websocket)
        # If the profit percentage is greater than the desired gains or below the stop loss, sell
        if percent_difference > float(percent_wanted) or percent_difference < -float(percent_loss_limit):
            print(f"{asset} sell signal due to basic sell scan")
            await websocket.close()
            return True


'''
 Ladder ascending profit sell scan: when the percentage gain is wanted, rather than sell right away, start a timer to
 see if it gains more than the positive step gain percentage within that timer, otherwise, sell. If the percentage
 increases above the step gain, reset the timer and wait again to see if it stagnates or keeps increasing. If the 
 percentage is dropped below the original percent wanted at any time, sell immediately. If a higher percentage is found
 and you are up a rung, the negative step gain determines if you sell based on a percent loss relative to that new 
 percentage gain. Example: Bought price 100. Goes to 105, sell scan initiates and waits the timer value before selling.
 If the positive step gain is set to 1, if the asset price goes to 106, then the timer resets. If the timer runs out and
 no more than a 5-6% gain is achieved, the sell order is initiated. If the asset jumps to 107, and the negative step 
 gain is set to 0.5, or half a percent, if the asset price drops to 106.5, it will sell before the timer expires. The
 timer value is set with hh:mm:ss format. This value may be modified in the future for less than second transactions
 and faster trades. Step sensitivity value sets the number to divide the positive and negative step values by each time
 the timer is reset and a step in profit is gained. This makes the algorithm more sensitive to the profits dropping the
 higher you go. The timer sensitivity value does the same thing but to the timer before it idles out and sells. Both 
 sensitivity values are optional. If you want to basically hold on to the asset for long until the the negative value is
 what triggers the sell to hold onto as long as possible, just set the timer value to many hours.
'''


async def ladder_sell_scan(asset, bought_price, percent_wanted, percent_loss_limit, positive_step_gain,
                           negative_step_gain,
                           timer_duration, sleep_duration=2, step_sensitivity_value=1, timer_sensitivity_value=1):
    negative_step_gain = -negative_step_gain
    sell_signal = False
    timer_started = False
    change_difference = 0
    websocket = await connect_websocket()
    while not sell_signal:
        # Calculates the potential profit or loss percentage
        percent_changed = await current_percent_difference(asset, bought_price, websocket)
        # If the percentage profit goes over the percent wanted, begin the ladder
        if percent_changed > percent_wanted and not timer_started:
            # Start the timer, start a while loop that stays on while the timer is going
            end_time = time.time() + time_to_seconds(timer_duration)
            timer_started = True
            print("Timer started in ladder sell scan as percent wanted has been achieved...")

        if timer_started:
            # If the timer expires after the percent wanted has been reached, sell
            if time.time() >= end_time:
                sell_signal = True
                print(f"{asset} sell signal due to timer expiring in ladder sell scan")
                return sell_signal
            else:
                time.sleep(sleep_duration)
                # Select the highest percentage profit the asset has reached and use it to calculate the difference
                greater_difference = max(percent_changed, change_difference)
                new_percent_difference = await current_percent_difference(asset, bought_price,
                                                                          websocket) - greater_difference
                # If the positive step gain is reached, reset the time, recalculate the sensitivity values if given
                if new_percent_difference > positive_step_gain:
                    print("New percent greater than step gain!")
                    change_difference = percent_changed + new_percent_difference
                    if step_sensitivity_value != 1:
                        positive_step_gain = positive_step_gain / step_sensitivity_value
                        negative_step_gain = negative_step_gain / step_sensitivity_value
                    if timer_sensitivity_value == 1:
                        end_time = time.time() + time_to_seconds(timer_duration)
                    else:
                        end_time = time.time() + time_to_seconds(timer_duration / timer_sensitivity_value)
                # If the negative step value is hit, initiate a sell order
                elif new_percent_difference < negative_step_gain:
                    sell_signal = True
                    print(f"{asset} sell signal due to negative step gain")
                    return sell_signal
        elif percent_changed <= -percent_loss_limit:
            sell_signal = True
            print(f"{asset} sell signal due to percent loss limit...")
            return sell_signal


if __name__ == '__main__':
    pass
