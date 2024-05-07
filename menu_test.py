import click

# Options that become required only if other options are called
OPTION_DEPENDENCIES = {
    'basic_buy': ['basic_buy_price'],
    'rsi_buy': ['rsi_buy_number', 'rsi_wait_period'],
    'basic_sell': ['basic_sell_profit'],
    'ladder': ['minimum_ladder_profit', 'ladder_step_gain', 'ladder_step_loss', 'ladder_timer_duration',
               'ladder_step_sensitivity', 'ladder_timer_sensitivity'],
    'swing_trade': ['swing_trade_skim']
}


# If an option is called that needs additional dependencies, add it to the list of missing options
def validate_dependent_options(ctx, param, value):
    missing_options = []
    # Value is the name of the click context value, so that's why I'm using value for the key name
    if value in OPTION_DEPENDENCIES.keys():
        click.echo(f"\nMissing the following options required for {value}:")
        for option in OPTION_DEPENDENCIES[value]:
            if option not in ctx.params:
                click.echo(option)
                missing_options.append(option)
        raise click.BadParameter(f"With the {param.name} option, please supply the above stated options.")



@click.command()
@click.option("--bot_type",
              required=True,
              type=click.Choice(["exchange", "atomic", "notifier"]),
              help="Specify the type of bot")
@click.option("--asset",
              required=True,
              type=click.Choice(["bitcoin", "ethereum", "solana", "xrp", "cardano", "dogecoin", "shiba-inu", "monero"]),
              help="Specify the crypto asset to buy and sell")
@click.option("--capital",
              required=True,
              type=click.Choice(["dollars", "tether", "usdc", "dai"]),
              help="The type of capital you wish to buy the asset with and sell the asset for")
@click.option("--start_type",
              required=True,
              type=click.Choice(["buy", "sell", "previous"]),
              help="The starting order type")
@click.option("--buy_order_type",
              required=True,
              type=click.Choice(["basic_buy", "rsi_buy"]),
              callback=validate_dependent_options,
              help="The type of buy order scan type you'd like to monitor the asset with to alert a buy signal")
@click.option("--sell_order_type",
              required=True,
              type=click.Choice(["basic_sell", "ladder"]),
              callback=validate_dependent_options,
              help="The type of sell order scan type you'd like to  monitor the asset with to alert a sell signal")
# Possibly refactor the name to stop_loss_limit later
@click.option("--percent_loss_limit",
              required=True,
              type=float,
              help="The percent you will allow your initial buy capital to drop by before selling at a loss"
              )
@click.option("--profit_loss_function",
              required=True,
              type=click.Choice(["profit_harvest", "swing_trade"]),
              callback=validate_dependent_options,
              help="The profit/loss reallocation protocol determining what to do with profits and losses post sell")
@click.option("--initial_capital",
              required=True,
              type=float,
              help="Specify the initial amount of capital you wish to place your buy order"
              )
# Additional options that could become required
# If basic buy
@click.option("--basic_buy_price",
              required=False,
              type=float,
              help="The price of the asset you want to buy at as an integer or float"
              )
# If RSI buy
@click.option("--rsi_buy_number",
              required=False,
              type=float,
              help="The RSI you'd like to sell at if it stays at that RSI for the wait period")
@click.option("--rsi_wait_period",
              required=False,
              # Use a time check function
              # type=click.Choice(),
              help="The amount of time to wait before the sell order is placed if an RSI is hit")
# If basic sell
@click.option("--basic_sell_profit",
              required=False,
              type=float,
              help="The percentage of profit you would like to achieve before the sell signal is true"
              )
# If ladder sell function
@click.option("--minimum_ladder_profit",
              required=False,
              type=float,
              help="The minimum profit percent you want before the sell time begins for the ladder profit sell function"
              )
@click.option("--ladder_step_gain",
              required=False,
              type=float,
              help="The percentage of each step to reset the timer at once the minimum profit has been reached"
              )
@click.option("--ladder_step_loss",
              required=False,
              type=float,
              help="The percentage drop step that will trigger an immediate sell in the ladder function"
              )
@click.option("--ladder_timer_duration",
              required=False,
              help="The duration of time to let the price stagnate before you sell. Format of 00:00:00 for hours, "
                   "minutes, and seconds, minutes and seconds being between 0-59"
              )
# use check time function
@click.option("--ladder_step_sensitivity",
              required=False,
              type=float,
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
              type=float,
              help="The percentage of profit you want to skim off to keep and not use to be swing traded."
              )
# Take every argument passed from click and make a key of the argument name and value of the argument value
def one_liner_values(**kwargs):
    return kwargs


# user_inputs = {arg_name: arg_value for arg_name, arg_value in kwargs.items()}
if __name__ == '__main__':
    one_liner_values()

# python3 menu_test.py --bot_type exchange --asset bitcoin --capital dollars --start_type buy --buy_order_type rsi --sell_order_type ladder --percent_loss_limit 10 --profit_loss_function profit_harvest --initial_capital 100
