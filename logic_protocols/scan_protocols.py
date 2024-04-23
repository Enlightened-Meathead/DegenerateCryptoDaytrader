# Scans that repeatedly look for the desired outcome and returns the value based on the asset given

import time
import asyncio
import websockets
import json
import requests
from bs4 import BeautifulSoup

import data_urls


asset_ticker_pair = {'bitcoin': 'BTC', 'ethereum': 'ETH', 'solana': 'SOL', 'xrp': 'XRP', 'cardano': 'ADA',
                     'dogecoin': 'DOGE', 'shiba-inu': 'SHIB', 'monero': 'XMR'
                     }


def time_to_seconds(time_string):
    # Splits the hh:mm:ss format into seconds
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

# RSI asset scan : returns the current RSI for the asset for the user defined span of time
# For now, just start with hourly RSI calculation to estimate RSI for the past 14 hours, experiment with time intervals
# later.
def rsi_scan(asset, time_span):
    # Go out on the internet and gather the RSI for the asset based on the time frame specified
    # initiate RSI
    page_to_scrape = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    html_rsi = soup.find('tr', attrs={'class': "datatable_cell__LJp3C !border-t-[#e6e9eb] !py-3 ltr:!text-right rtl:soft-ltr"})
    return html_rsi

# Asynchronous websocket connection through coinbase that returns the price of the given ticker pair every 5 seconds
async def persistent_price_scan(asset):
    uri = "wss://ws-feed.exchange.coinbase.com"
    price_pair = asset_ticker_pair[asset] + '-USD'
    subscribe_message = json.dumps({
        "type": "subscribe",
        "product_ids": [price_pair],
        "channels": ["ticker_batch"]
    })
    async with websockets.connect(uri) as websocket:
        await websocket.send(subscribe_message)
        print("Websocket  connection established")
        while True:
            response = await websocket.recv()
            json_response = json.loads(response)
            # Check if message is a ticker message then parse the price
            if 'type' in json_response and json_response['type'] == 'ticker' and 'price' in json_response:
                price = json_response['price']
                return price

def current_price_scan():
    return True

print(asyncio.run(persistent_price_scan('ethereum')))

# Calculate the difference in percentage from the price bought to the current value of the asset
def current_percent_difference(bought_price):
    percent_difference = ((float(current_price_scan()) / bought_price) - 1) * 100
    return percent_difference


'''
 Basic sell scan: given the users desired percentage gain from the bought price, send true once that percentage is met
 Bought price is the price you bought it originally, percent wanted is the float number percentage, ie 5.5% is just
 5.5, and percent loss limit is the whole float number percentage started with a  negative value, ie 2.2% max loss 
 before you sell is -2.2
'''


def basic_sell_scan(bought_price, percent_wanted, percent_loss_limit):
    # While the percent wanted is not equal to the current potential profit, set sell signal to false
    sell_signal = False
    while not sell_signal:
        # Calculates the potential profit or loss percentage
        percent_difference = current_percent_difference(bought_price)
        # If the profit percentage is greated than the desired gains or below the stop loss, sell
        if percent_difference > percent_wanted or percent_difference < percent_loss_limit:
            sell_signal = True
            return sell_signal
    return current_percent_difference


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


def ladder_sell_scan(bought_price, percent_wanted, percent_loss_limit, positive_step_gain, negative_step_gain,
                     timer_duration, sleep_duration, step_sensitivity_value=1, timer_sensitivity_value=1):
    sell_signal = False
    timer_started = False
    change_difference = 0
    while not sell_signal:
        # Calculates the potential profit or loss percentage
        percent_changed = current_percent_difference(bought_price)

        # If the percentage profit goes over the percent wanted, begin the ladder
        if percent_changed > percent_wanted and not timer_started:
            # Start the timer, start a while loop that stays on while the timer is going
            end_time = time.time() + time_to_seconds(timer_duration)
            timer_started = True

        if timer_started:
            # If the timer expires after the percent wanted has been reached, sell
            if time.time() >= end_time:
                sell_signal = True
                print("Sold due to timer expiring")
                return sell_signal
            else:
                time.sleep(sleep_duration)
                # Select the highest percentage profit the asset has reached and use it to calculate the difference
                greater_difference = max(percent_changed, change_difference)
                new_percent_difference = current_percent_difference(bought_price) - greater_difference
                # If the positive step gain is reached, reset the time, recalculate the sensitivity values if given
                if new_percent_difference > positive_step_gain:
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
                    print("sold due to negative step gain")
                    return sell_signal
        elif percent_changed <= percent_loss_limit:
            sell_signal = True
            print("sold due to percent loss limit")
            return sell_signal
        time.sleep(sleep_duration)
