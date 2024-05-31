Variables to be gathered from the user:
--asset : the crypto to trade
--capital : the crypto or asset to sell into
--start_type : buy or sell. Sets the scan order depending on your current position.
--buy_order_type : the type of buy order, the two I have so far are basic_buy and rsi_buy
For the basic buy, you need to set a price you want to buy the asset at and for the RSI buy you need to set the RSI
you would like to buy at, the time span it needs to remain in that RSI, the RSI drop limit of how low you're willing
to let the RSI drop below your minimum, and then the wait period between scanning for the RSI
--sell_order_type : the type of sell order, the two currently available are basic_sell, which requires a desired
percentage of profit gained and a stop loss percentage. The other is ladder_sell, which requires initial percent
wanted profit gain, step percent gain, stop loss percentage, negative step gain, the timer duration, the step
sensitivity value, and the timer sensitivity value
--profit_loss_function : the profit loss reallocation function, two option rn are profit harvest and swing trade. For
profit harvest, you must set the if you want the full amount sold or just the profit you specified in the sell order
type. If you choose swing trade, you need to pass the skim percent which is an integer of 1-100 as the percent of
the profit you want to keep and NOT be used to swing trade.
--initial_capital : the set amount to trade with you are using to buy each time if you profit harvest or the amount you
are starting with in your swing trading.
--minimum_capital : optional, if the amount the account drops below the amount you set here, notify you and withhold further trade