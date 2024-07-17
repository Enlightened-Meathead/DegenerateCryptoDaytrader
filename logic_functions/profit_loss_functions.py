# Functions that calculate profit or loss and reallocates assets once a trade is made
import asyncio
import logic_functions.scan_functions as scf


# Little function that return the profit or loss percentage in decimal form, ie 10% == 0.10
async def profit_loss_percent(asset, bought_price):
    websocket = await scf.connect_websocket()
    profit_percent = float(await scf.current_percent_difference(asset, bought_price, websocket)) * 0.01
    await websocket.close()
    return profit_percent


# If a full sell is not made, calculate the profit or loss relative to the proportion sold and
def dollar_profit_loss(asset_amount_sold, bought_price, sold_price):
    sold_portion_cost = bought_price * asset_amount_sold
    sold_portion_revenue = sold_price * asset_amount_sold
    profit_loss = sold_portion_revenue - sold_portion_cost
    return profit_loss


"""
 Fixed asset buy profit harvesting P/LRP: when a sell is made, any profit kept, and the fixed amount set to trade with
 is used to buy the next position. For example, when you set $100 to trade, if you sell for $105, $5 is kept and $100
 will be used for the next buy position. You can set if you want to just sell the profit and keep your position, or sell
 the entire position and initiate a new buy function to prevent only being sold once the stop limit is reached.
"""


def profit_harvest(asset, bought_price, amount_bought, full_sell=False):
    # Calculate the profit gained. Multiply that percentage by the current price to calculate profit
    if not full_sell:
        profit_loss = asyncio.run(profit_loss_percent(asset, bought_price))
        profit_to_sell = float(amount_bought) * float(profit_loss)
        # Return the dollar amount to sell
        print(f"Profit_to_sell: {profit_to_sell}")
        return profit_to_sell
    else:
        # If a full sell is selected, sell the entire position
        return 'sell_all'


"""
 Swing trading P/LRP: Use the profits from trades to increase capital for buys, this could theoretically maximize
 profits, but also maximizes losses for large dips. If you plan to do this, keep a tax treasury fund as if you swing
 trade massive amounts, even if you lose it all on a dip, you still owe tax on the short term capital gains, or 15% of
 profit I.E. if you trade from $10,000 up to $100k, $90,000 profit will likely be taxed at minimum 15%, or $13,500. If
 you end up losing it all because you majorly gamble, and drop back down to $10,000 only, capital loss is only a max of
 $3k per year, and you'd still owe $10.5k even if you don't have the money. Swing trading is risky with large amounts,
 be warned. I am not a financial advisor and this is not financial advice. Just giving you a head up, so you don't
 screw over your life by being an ignorant donkey.
"""


def swing_trade(amount_bought, amount_sold, skim_percent=0):
    # If a portion of the profit is wanted to be kept, calculate that
    profit_to_keep = 0
    if skim_percent > 0:
        profit_to_keep = (float(amount_sold) - float(amount_bought)) * (skim_percent * 0.01)
    # Return the amount in to use for the next buy order
    next_buy_amount = amount_sold - profit_to_keep
    print(f"next_buy_amount: {next_buy_amount}")
    return next_buy_amount


if __name__ == "__main__":
    #asyncio.run(profit_loss_percent('hedera', 0.066))
    #swing_trade(100, 250, 5)
    print(dollar_profit_loss(100, 10, 11, ))

    pass
