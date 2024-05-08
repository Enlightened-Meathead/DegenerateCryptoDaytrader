# CLI based user input menu for people who don't know how to run the program with a one-liner,
# as well as a parser for a one-liner of options to pass to the bot
import click
import subprocess

menu_banner = """
$$$$$$                                                                
$     $ $$$$$$  $$$$  $$$$$$ $    $ $$$$$$ $$$$$    $$   $$$$$ $$$$$$ 
$     $ $      $    $ $      $$   $ $      $    $  $  $    $   $      
$     $ $$$$$  $      $$$$$  $ $  $ $$$$$  $    $ $    $   $   $$$$$  
$     $ $      $  $$$ $      $  $ $ $      $$$$$  $$$$$$   $   $      
$     $ $      $    $ $      $   $$ $      $   $  $    $   $   $      
$$$$$$  $$$$$$  $$$$  $$$$$$ $    $ $$$$$$ $    $ $    $   $   $$$$$$ 
                                                                      
 $$$$$                                   
$     $ $$$$$  $   $ $$$$$  $$$$$  $$$$  
$       $    $  $ $  $    $   $   $    $ 
$       $    $   $   $    $   $   $    $ 
$       $$$$$    $   $$$$$    $   $    $ 
$     $ $   $    $   $        $   $    $ 
 $$$$$  $    $   $   $        $    $$$$  
                                         
$$$$$$                                                        
$     $   $$   $   $ $$$$$ $$$$$    $$   $$$$$  $$$$$$ $$$$$  
$     $  $  $   $ $    $   $    $  $  $  $    $ $      $    $ 
$     $ $    $   $     $   $    $ $    $ $    $ $$$$$  $    $ 
$     $ $$$$$$   $     $   $$$$$  $$$$$$ $    $ $      $$$$$  
$     $ $    $   $     $   $   $  $    $ $    $ $      $   $  
$$$$$$  $    $   $     $   $    $ $    $ $$$$$  $$$$$$ $    $ 

==================================================================
BEFORE USING THIS PROGRAM, READ THE DOCUMENTATION AND/OR MAN PAGE!
==================================================================
"""
# Function to check if the user needs additional options based on primary option inputs

'''
def validate_additonal_options(ctx, param, value):
    # If the value of the options is in a list of required options and that required option must have additional values,
    # make the value of the next option it needs to be required.
    additional_requirements = [
        "basic_buy", "rsi", "basic_sell", "ladder", "profit_harvest", "swing_trade",
    ]
    if value is not None:
        pass

# Function to check if the user passed no minimum capital or if they did enter a value convert it a float
def validate_minimum_capital(ctx, param, value):
    if value.lower() == "no":
        return value.lower()
    try:
        return float(value)
    except ValueError:
        raise click.BadParameter("Minimum capital must be 'no' or a numeric value.")

'''
@click.command()
@click.argument("menu",
                type=click.Choice(["menu", "nomenu"]), default="menu",
                help='Specifies to whether skip the interactive menu if you want to use an aliased one liner')
@click.option("--bot_type",
              type=click.Choice(["exchange", "atomic", "notifier"]),
              help="Specify the type of bot")
@click.option("--asset",
              type=click.Choice(["bitcoin", "ethereum", "solana", "xrp","cardano", "dogecoin","shiba-inu", "monero"]),
              help="Specify the crypto asset to buy and sell")
@click.option("--capital",
              type=click.Choice(["dollars", "tether", "usdc", "dai"]),
              help="The type of capital you wish to buy the asset with and sell the asset for")
@click.option("--start_type",
              type=click.Choice(["buy", "sell", "previous"]),
              help="The starting order type")
@click.option("--buy_order_type",
              type=click.Choice(["basic_buy", "rsi"]),
              help="The type of buy order scan type you'd like to monitor the asset with to alert a buy signal")
@click.option("--sell_order_type",
              type=click.Choice(["basic_sell", "ladder"]),
              help="The type of sell order scan type you'd like to  monitor the asset with to alert a sell signal")
# Possibly refactor the name to stop_loss_limit later
@click.option("--percent_loss_limit",
              type=(float, int),
              help="The percent you will allow your initial buy capital to drop by before selling at a loss"
              )
@click.option("--profit_loss_function",
              type=click.Choice(["profit_harvest", "swing_trade"]),
              help="The profit/loss reallocation protocol determining what to do with profits and losses post sell")
@click.option("--initial_capital",
              type=(float, int),
              help="Specify the initial amount of capital you wish to place your buy order"
              )

'''
@click.option("--minimum_capital",
              callback=validate_minimum_capital,
              help="Specify the minimum you want your capital to drop to before you stop trading or enter 'no' for no"
                   "minimum")
'''
'''
# Additional options that could become required
# If basic buy
@click.option("--basic_buy_price",
              required=False,
              type=(float, int),
              help="The price of the asset you want to buy at as an integer or float"
              )
# If RSI buy 
@click.option("--rsi_buy_number",
              required=False,
              type=(float, int),
              help="The RSI you'd like to sell at if it stays at that RSI for the wait period")
@click.option("--rsi_wait_period",
              required=False,
              # Use a time check function
              # type=click.Choice(),
              help="The amount of time to wait before the sell order is placed if an RSI is hit")
# If basic sell
@click.option("--basic_sell_profit",
              required=False,
              type=(int, float),
              help="The percentage of profit you would like to achieve before the sell signal is true"
              )
#If ladder profit loss function
@click.option("--minimum_ladder_profit",
              required=False,
              type=(float, int),
              help="The minimum profit percent you want before the sell time begins for the ladder profit sell function"
              )
@click.option("--ladder_step_gain",
              required=False,
              type=(float, int),
              help="The percentage of each step to reset the timer at once the minimum profit has been reached"
              )
@click.option("--ladder_step_loss",
              required=False,
              type=(float, int),
              help="The percentage drop step that will trigger an immediate sell in the ladder function"
              )
@click.option("--ladder_timer_duration",
              required=False,
              help= "The duration of time to let the price stagnate before you sell. Format of 00:00:00 for hours, "
                    "minutes, and seconds, minutes and seconds being between 0-59"
              )
              # use check time function
@click.option("--ladder_step_sensitivity",
              required=False,
              type=(float, int),
              help="The number to divide the step gain and loss percentage to make the number more sensitive the higher"
                   "the profit goes"
              )
@click.option("--ladder_timer_sensitivity",
              required=False,
              help="The number to divide the ladder timer duration by to increase or decrease the time period to sell "
                   "after"
              )
# If profit loss swing trade
@click.option("--swing_trade_skim",
              required=False,
              type = (float, int),
              help="The percentage of profit you want to skim off to keep and not use to be swing traded."
              )
'''
'''


def test():
    print(menu_banner)
    user_inputs = {}
    bot_type = click.prompt("What type of bot are you going to use?\nAutomated is using an exchange and API key for "
                            "automated trades on that exchange.\nAtomic will use the atomic wallet GUI with atomic "
                            "swaps for the trade.\nNotifier will just send notifications.",
                            type=click.Choice(["exchange", "atomic", "notifier"]))
    # If bot type is exchange, display available exchanges, have them enter an API key and necessary creds
    # If atomic, select resolution and tell them to run the test to make sure it will work.
    # If notifier, have them select how they would like to be notified: desktop, email?,sms?, some other notification?
    # For now, start with notifier and just send desktop notifications
    asset = click.prompt("Select an asset to trade",
                         type=click.Choice(["bitcoin", "ethereum", "solana", "xrp",
                                            "cardano", "dogecoin", "shiba-inu", "monero"]))
    capital = click.prompt("Select the capital you'd like to sell to",
                           type=click.Choice(["dollars", "tether", "usdc", "dai"]))
    start_type = click.prompt("Select if you are starting with a buy, sell, or previous trade",
                              type=click.Choice(["buy", "sell", "previous"]))
    # If previous, lookup log of open buys from the spreadsheet and confirm which asset amount to use
    buy_order_type = click.prompt("Select a buy order type", type=click.Choice(["basic_buy", "rsi"]))
    # If basic, have the user input the price to buy the asset at. If RSI, have the user enter the RSI they want to
    # buy at, a wait period to buy after the RSI is still below the RSI they specified, to buy at if the wait period
    # expires, and the RSI drop limit
    sell_order_type = click.prompt("Select a sell order type", type=click.Choice(["basic_sell", "ladder"]))
    # If basic, have the user enter the profit percentage to sell at and the stop loss percentage
    # If ladder, have the user enter the in the minimum profit percent they want to sell at, the stop loss percent,
    # the positive step gain percentage, the negative step gain percentage, the timer duration to wait to see if the
    # price will stagnate then to sell, the step sensitivity value, and the timer sensitivity value.
    profit_loss_function = click.prompt("Select the profit loss reallocation function",
                                        type=click.Choice(["profit_harvest", "swing_trade"]))
    # If profit harvest, ask if they want a full sell or just the portion of the profits
    # If swing trade, ask what percentage of the profits they would like to skim off from the sells.
    initial_capital = click.prompt("How much capital you would like to buy in dollars")
    minimum_capital = click.prompt("Would you like to set a minimum that you will allow your capital to dip that would "
                                   "trigger the bot to abort any further trades?",
                                   type=click.Choice(["yes", "no"]))

    "Enter the lowest dollar amount you are willing to let your capital dip to before "
    "aborting the trade bot?\n You can enter a float with a decimal point, i.e. 250.50, "
    "or an integer i.e. 100. None is no bottom limit",
'''