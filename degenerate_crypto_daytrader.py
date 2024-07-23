# # The main program file. The click library has some goofy behavior that requires alot of these functions to be in
# the same module, and after being way too deep in the project I learned click probably wasn't the best choice,
# so this module is what it is :P

# Standard Library
import asyncio
import re
import time
from datetime import datetime

# Community library for creating CLI text based applications and parsing arguments and command options
import click

# Local module imports
from logic_functions import logging_functions as lof
from logic_functions import profit_loss_functions as plf
from logic_functions import scan_functions as scf
from logic_functions import notify_functions as nof
from order_class import Order

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
# Right now, for one-liners make sure any additional option dependencies are declared before their parent option

# Options that become required only if other options are called
OPTION_DEPENDENCIES = {
    'basic_buy': ['basic_buy_price'],
    'rsi_buy': ['rsi_buy_number', 'rsi_drop_limit', 'rsi_wait_period'],
    'basic_sell': ['basic_sell_profit'],
    'ladder': ['minimum_ladder_profit', 'ladder_step_gain', 'ladder_step_loss', 'ladder_timer_duration',
               'ladder_step_sensitivity', 'ladder_timer_sensitivity'],
    'swing_trade': ['swing_trade_skim'],
    'sell': ['asset_bought_price', 'sell_order_type', 'percent_loss_limit'],
    'buy': ['buy_order_type'],
}
REQUIRED_OPTIONS = ['bot_type', 'asset', 'capital', 'start_type',
                    'profit_loss_function', 'initial_capital', 'log_trade']

total_missing_options = []
menu_assigned_options = {}
final_user_options = {}
selected_user_options = {}
click_objects_dict = {}

def check_for_config():
    pass

# If an option is called that needs additional dependencies, add it to the list of missing options
def validate_dependent_options(ctx, param, value):
    global total_missing_options
    missing_options = []
    # Value is the name of the click context value, so that's why I'm using value for the key name
    if value in OPTION_DEPENDENCIES.keys() and ctx.params.get("menu") != "menu":
        for option in OPTION_DEPENDENCIES[value]:
            # If an option required by the parent option is not present, make it required
            if option not in ctx.params:
                total_missing_options.append(option)
                print(total_missing_options)
                missing_options.append(option)
        # Print out all missing options the user didn't pass on the command line
        if len(missing_options) > 0:
            click.echo(f"\nWith the {value} choice for the {param.name} option, please supply the below stated"
                       f" additionally required options:\n--------------------------")
            for option in missing_options:
                click.echo(option)
            click.echo("\nWhen adding the above to your one liner, place these BEFORE the option that triggers these "
                       "dependencies.")
    return value


# Callback for the menu argument that makes options required if the no_menu argument is passed
def make_required(ctx, param, value):
    global REQUIRED_OPTIONS
    if value == "no_menu":
        # If the user wants no menu, then make every option needed to be required in click.
        for option in REQUIRED_OPTIONS:
            for param in ctx.command.params:
                if param.name == option:
                    param.required = True


# Check to see if there are any missing options. If so, abort the program.
def check_missing_options():
    global total_missing_options
    if total_missing_options:
        return True


def set_dependency_options(option_dependency, ctx):
    global menu_assigned_options
    dependency_option = next(
        (opt for opt in ctx.command.params if opt.name == option_dependency), None)
    dependency_user_input = click.prompt(f"{dependency_option.help}",
                                         type=dependency_option.type)
    menu_assigned_options[dependency_option.name] = dependency_user_input
    return dependency_user_input


# Recursive function that checks if menu input has dependency then check if that dependency input has dependencies, etc
def menu_dependency_check(user_input, ctx):
    global OPTION_DEPENDENCIES
    if user_input in OPTION_DEPENDENCIES.keys():
        # For every dependency for the user input option
        for option_dependency in OPTION_DEPENDENCIES[user_input]:
            # Check if the dependency was passed at the command line, if not, prompt the user to add it.
            if option_dependency not in ctx.params.keys():
                dependency_user_input = set_dependency_options(option_dependency, ctx)
                menu_dependency_check(dependency_user_input, ctx)


'''
For the menu, for every option, create a prompt with the message being the help message, the click choices the 
prompt choice, then make the answer to that prompt equal to the parameter value for that parameters name then pass 
that option to click. If the program is called with menu and some options, start the menu but only for their missing 
options - say the user is missing some options, and tell them if they dont want this menu pass the argument no menu - 
check if the passed options require optional dependencies. for every global total missing option, prompt the user to 
enter them
'''


# IF YOU ENTER THE MENU OPTION AS THE FIRST OPTION PASSED, NO ARGUMENTS GET PASSED TO CLICK
#  CLI menu that parses user input for the required options not passed on the command line
def click_menu(ctx, param, value):
    global REQUIRED_OPTIONS
    global total_missing_options
    global menu_assigned_options
    make_required(ctx, param, value)
    if value == 'menu':
        click.echo(menu_banner)
        for option in ctx.command.params:
            # For every option in the click command that hasn't been given a value yet and is required:
            if option.name not in ctx.params.keys() and option.name in REQUIRED_OPTIONS:
                user_input = click.prompt(f"{option.help}", type=option.type)
                # If the user input has associated dependencies
                menu_dependency_check(user_input, ctx)
                menu_assigned_options[option.name] = user_input

        # If any missing options exist from the command line, prompt the user for those as well
        click.echo("The following are required additional options based on some of your options you passed on the "
                   "command line:")
        # For the missing options that weren't passed at the command line with the option that requires them
        for option in total_missing_options:
            # Get the option object that was missing from the command line and prompt the user
            set_dependency_options(option, ctx)
    return value


# Check if the user input is an integer or the string 'cancel' to escape the modify loop
def integer_or_cancel(user_input):
    try:
        return int(user_input)
    except ValueError:
        if user_input == "cancel":
            return user_input


#
def finalize_dependent_options(changed_option_value):
    global final_user_options
    global click_objects_dict
    global OPTION_DEPENDENCIES
    dependency_options = OPTION_DEPENDENCIES[changed_option_value]
    for option in dependency_options:
        dependency_choice = click_objects_dict[option]
        changed_option_value = click.prompt(f'Enter new value for {option}', type=dependency_choice)
        final_user_options[option] = changed_option_value
        if changed_option_value in OPTION_DEPENDENCIES.keys():
            finalize_dependent_options(changed_option_value)
    print(final_user_options)


# Could definitely be optimized, but for now its functional
"""
This big kahuna is a user review menu that takes the user inputs from the command line and menu then lets them 
review them and update them. Once the user confirms their final settings, it takes all the user inputs and converts 
them to a one-liner they can copy paste if they want to run the same trade and stores it into a command history log 
file for this program. The reason this function is so massive is because I was struggling to pass the click context 
to multiple functions without issues so here we are for now with this abomination. Future refactor material!
"""


def finalize_user_inputs():
    global final_user_options
    global click_objects_dict
    global selected_user_options
    global OPTION_DEPENDENCIES
    modify_choice_dict = {}
    confirm_choices = 'no'
    # While the user has not confirmed their settings, present them the option to change things
    while confirm_choices == 'no':
        option_index = []
        print("\n===========================\nYour current option values:\n===========================")
        # Create a numbered index of values the user needs so they can reference a number rather than type the entire
        # name they want to change
        for key, value in final_user_options.items():
            if value is not None:
                option_index.append(key)
                selected_user_options[key] = value
                print(f"{option_index.index(key) + 1}: {key} = {value}")
                modify_choice_dict[option_index.index(key) + 1] = key
        modify_choice = click.prompt("Would you like to modify any option's values?",
                                     type=click.Choice(['yes', 'no']))
        # Added this flag so if the user says 'no' to changing values the user settings don't double print themselves
        display_options = False
        while modify_choice == 'yes':
            display_options = True
            # Get the length of the index of choices and make it into a list of the range of integers
            choice_length = range(0, len(option_index))
            # Create a list of the valid range the user can enter as an option to modify
            choices_range = [(choice + 1) for choice in choice_length]
            invalid_choice = True
            user_int = 0
            # Get the number of the option within the index the user wants to modify
            while invalid_choice:
                user_int = click.prompt(
                    'Please enter which option-value pair you would like to change (Enter a number from '
                    'the index or cancel to cancel)', type=integer_or_cancel
                )
                if user_int == 'cancel':
                    invalid_choice = False
                    modify_choice = 'no'
                elif user_int not in choices_range:
                    print(f"Please enter a valid integer within the range 1 to {len(option_index)}")
                else:
                    invalid_choice = False
            if modify_choice == 'yes':
                # Prompt the user for the choice at that index then update that choice in the final_user_options
                # Get the name of the option corresponding with the index number
                user_option_change = modify_choice_dict[user_int]
                # Get the choices object from the dictionary of options and their corresponding choices
                change_choices = click_objects_dict[user_option_change]
                # Convert the change_choices object into a list to use as the choices for the prompt
                try:
                    choice_list = [choice for choice in change_choices.choices]
                except AttributeError:
                    # If the choice for the choice object is non-iterable such as a float or percentage and uses a
                    # callback or type, make the choice list just use that type check function
                    choice_list = change_choices

                # If the choice list is a list, make that the type
                if isinstance(choice_list, list):
                    changed_option_value = click.prompt(f'Enter new value for {user_option_change}',
                                                        type=click.Choice(choice_list))
                else:
                    changed_option_value = click.prompt(f'Enter new value for {user_option_change}',
                                                        type=choice_list)
                # Update the final list of options with the changed value
                final_user_options[user_option_change] = changed_option_value
                # Check to see if the updated option adds any dependent options, and if that's the case, prompt the user
                if changed_option_value in OPTION_DEPENDENCIES.keys():
                    dependency_options = OPTION_DEPENDENCIES[changed_option_value]
                    for option in dependency_options:
                        dependency_choice = click_objects_dict[option]
                        changed_option_value = click.prompt(f'Enter new value for {option}', type=dependency_choice)
                        final_user_options[option] = changed_option_value
                        if changed_option_value in OPTION_DEPENDENCIES.keys():
                            dependency_options = OPTION_DEPENDENCIES[changed_option_value]
                            for dependency_option in dependency_options:
                                dependency_choice = click_objects_dict[dependency_option]
                                changed_option_value = click.prompt(f'Enter new value for {dependency_option}',
                                                                    type=dependency_choice)
                                final_user_options[dependency_option] = changed_option_value

        # Ask the user again if they want to anything, if no, make them type CONFIRM to start the bot with a prompt
        # that gives them a legal warning
        if display_options:
            print("\n===========================\nYour current option values:\n===========================")
            for key, value in final_user_options.items():
                if value is not None:
                    option_index.append(key)
                    selected_user_options[key] = value
                    print(f"{option_index.index(key) + 1}: {key} = {value}")
                    modify_choice_dict[option_index.index(key) + 1] = key
        confirm_choices = click.prompt("Are these are your final settings? If so, please type CONFIRM and the bot "
                                       "will start. If not, type no to go back and modify",
                                       type=click.Choice(['CONFIRM', 'no']))


# Type check function for the click options to make sure they meet the required format
def check_time_format(input_value):
    time_format = r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$'
    invalid_message = ("Invalid time. Please give a time with the format of HH:MM:SS. Example of 1 hour 30 minutes: "
                       "01:30:00")
    if re.match(time_format, input_value):
        return input_value
    else:
        raise click.BadParameter(invalid_message)


# Type check for the click options that makes sure the RSI and percentages are in range of 0-100
def check_percentage(input_value):
    invalid_message = "Invalid percentage. Please give a value between 0 and 100"
    if 100 >= float(input_value) >= 0:
        return input_value
    else:
        raise click.BadParameter(invalid_message)


# When you get to a point that you can natively interact with wallets and read funds, check to make sure the user
# has enough funds before trying to start a trade
def check_enough_capital(input_value):
    if float(input_value) > 0:
        return input_value
    else:
        raise click.BadParameter("Please enter a positive number of the value you wish to buy the trade with")


# Take the click command arguments passed at the command line and combine them with the menu assigned options
def merge_user_inputs(**kwargs):
    global menu_assigned_options
    global final_user_options
    global click_objects_dict
    global selected_user_options

    # Take every click option and make into a dictionary to be referenced for outside the scope of the click
    # command options that normally are only accessible directly read from the initial command line input
    ctx = click.get_current_context()
    for param in ctx.command.params:
        click_objects_dict[param.name] = param.type

    # If the user did not specify no_menu in the case of a one-liner, then give them a menu for any missing options
    # and to have them review and confirm their settings

    # Merge the click command line options with the menu options overwriting the click options
    final_user_options = kwargs | menu_assigned_options
    if ctx.params['menu'] == 'menu':
        # Menu, review page, dependency option checks, and finalize everything into a single dictionary
        finalize_user_inputs()
        lof.repeat_one_liner(selected_user_options)


# Pass the final user options to the Order class
def create_order_object():
    global final_user_options
    order = Order(
        bot_type=final_user_options['bot_type'],
        asset=final_user_options['asset'],
        capital=final_user_options['capital'],
        start_type=final_user_options['start_type'],
        percent_loss_limit=final_user_options['percent_loss_limit'],
        profit_loss_function=final_user_options['profit_loss_function'],
        initial_capital=final_user_options['initial_capital'],
        menu=final_user_options['menu'],
        log_trade=final_user_options['log_trade'],
        # Click already assigns optional inputs to None, but for clarity I added the .get and None for key errors
        buy_order_type=final_user_options.get('buy_order_type', None),
        sell_order_type=final_user_options.get('sell_order_type', None),
        asset_bought_price=final_user_options.get('asset_bought_price', None),
        basic_buy_price=final_user_options.get('basic_buy_price', None),
        basic_sell_profit=final_user_options.get('basic_sell_profit', None),
        swing_trade_skim=final_user_options.get('swing_trade_skim', None),
        rsi_buy_number=final_user_options.get('rsi_buy_number', None),
        rsi_drop_limit=final_user_options.get('rsi_drop_limit', None),
        rsi_wait_period=final_user_options.get('rsi_wait_period', None),
        minimum_ladder_profit=final_user_options.get('minimum_ladder_profit', None),
        ladder_step_gain=final_user_options.get('ladder_step_gain', None),
        ladder_step_loss=final_user_options.get('ladder_step_loss', None),
        ladder_timer_duration=final_user_options.get('ladder_timer_duration', None),
        ladder_step_sensitivity=final_user_options.get('ladder_step_sensitivity', None),
        ladder_timer_sensitivity=final_user_options.get('ladder_timer_sensitivity', None),
        history=final_user_options.get('history', None)
    )
    return order


# Scan for the given order object when to buy or sell
def buy_sell_signal_scan(order):
    buy_signal = False
    sell_signal = False
    # 2. Based on initial buy or sell scan, begin the scan protocol to buy or sell. Also, rescan if the user doesn't
    # reply in a certain amount of time or the user says to cancel and restart the scan
    if order.start_type == 'buy':
        if order.buy_order_type == 'basic_buy':
            buy_signal = asyncio.run(scf.basic_buy_scan(order.asset, order.basic_buy_price))
        elif order.buy_order_type == 'rsi_buy':
            buy_signal = scf.rsi_buy_scan(order.asset, order.rsi_buy_number, order.rsi_drop_limit,
                                          order.rsi_wait_period)
        if buy_signal:
            return 'buy'
    elif order.start_type == 'sell':
        if order.sell_order_type == 'basic_sell':
            sell_signal = asyncio.run(
                scf.basic_sell_scan(order.asset, order.asset_bought_price, order.basic_sell_profit,
                                    order.percent_loss_limit))
        if order.sell_order_type == 'ladder':
            sell_signal = asyncio.run(
                scf.ladder_sell_scan(order.asset, order.asset_bought_price, order.minimum_ladder_profit,
                                     order.percent_loss_limit, order.ladder_step_gain, order.ladder_step_loss,
                                     order.ladder_timer_duration, order.ladder_step_sensitivity,
                                     order.ladder_timer_sensitivity))
        if sell_signal:
            return 'sell'
    else:
        print("The program was unable to determine a buy or sell to start the trade. ABORTING!")
        exit()


# Create email message if buy signal is found
def buy_signal_email(order):
    print("Buy signal found!")
    current_price = asyncio.run(scf.current_price_scan(order.asset))
    amount_to_buy = order.initial_capital / order.asset_bought_price
    subject = 'DCDB'
    message = (
        f"Buy {amount_to_buy} {order.asset} for the current price of ${current_price} at "
        f"the time of this email")
    return subject, message


# Create email message if a sell signal is found
def sell_signal_email(order):
    print("Sell signal found!")
    amount_to_sell = 0
    order.amount_bought = order.initial_capital / order.asset_bought_price
    profit_loss_percent = asyncio.run(plf.profit_loss_percent(order.asset, order.asset_bought_price)) * 100
    if order.profit_loss_function == 'profit_harvest':
        # add in a user click option if they want a full sell for the profit harvest
        amount_to_sell = plf.profit_harvest(order.asset, order.asset_bought_price, order.amount_bought)
    elif order.profit_loss_function == 'swing_trade':
        current_price = asyncio.run(scf.current_price_scan(order.asset))
        amount_to_sell = order.initial_capital / current_price
        # Will be using this in the future
        # next_buy_amount = plf.swing_trade(order.amount_bought, amount_to_sell, order.swing_trade_skim)
    current_price = asyncio.run(scf.current_price_scan(order.asset))
    dollar_profit_loss = plf.dollar_profit_loss(order.asset_bought_price, current_price, amount_to_sell)
    subject = 'DCDS'
    message = (f"Sell {amount_to_sell} from your {order.amount_bought} {order.asset} according to your "
               f"selected {order.profit_loss_function} profit loss function for a current profit/loss of "
               f"{profit_loss_percent:.2f}% for ${dollar_profit_loss:.2f} of gains/losses")
    return subject, message


# Check if the user tells the program to wait, then if so restart the scan after the wait time
def check_if_wait(email_response_dict):
    if 'bot_time_to_wait' in email_response_dict.keys():
        wait_time = email_response_dict['bot_time_to_wait']
        print(f"Told to wait {wait_time}!")
        wait_time_seconds = scf.time_to_seconds(wait_time)
        time.sleep(wait_time_seconds)
        print("Restarting program after user wait period time expired...")
        run_program_procedure()


# Take the email response and see if the user wants to wait or if they made the trade. If they did, log the trade
def log_trade_check(email_response, order):
    email_response_parsed = nof.email_reply_parser(email_response)
    email_response_dict = nof.email_value_assigner(email_response_parsed)
    # if wait command in user response email, call the main program procedure after the wait period
    check_if_wait(email_response_dict)
    if order.log_trade == 'excel':
        lof.check_workbook_existence(lof.workbook_file_path)
        try:
            email_dollar_total = float(email_response_dict['email_dollar_total'])
            email_asset_amount = float(email_response_dict['email_asset_amount'])
            current_price = asyncio.run(scf.current_price_scan(order.asset))
            # I need to get the asset sold total and the asset amount sold from the user to correctly log it to
            # the spreadsheet, the user replied asset sold total should include fees already, so that's the real
            # returned value
            if order.start_type == 'sell':
                dollar_profit_loss = plf.dollar_profit_loss(order.asset_bought_price,
                                                            current_price,
                                                            email_asset_amount,
                                                            email_dollar_total)
                profit_loss_percent = asyncio.run(
                    plf.profit_loss_percent(order.asset, order.asset_bought_price)) * 100
                try:
                    lof.log_trade(datetime.now(),
                                  order.start_type,
                                  order.asset,
                                  order.asset_bought_price,
                                  order.amount_bought,
                                  float(order.asset_bought_price) * float(order.amount_bought),
                                  current_price,
                                  email_asset_amount,
                                  email_dollar_total,
                                  profit_loss_percent,
                                  dollar_profit_loss)
                    lof.calculate_totals()
                except FileNotFoundError:
                    print('Workbook does not exist! Check your config file and make sure the workbook exists.')
                    # Create workbook menu function
            elif order.start_type == 'buy':
                try:
                    lof.log_trade(datetime.now(),
                                  order.start_type,
                                  order.asset,
                                  current_price,
                                  email_asset_amount,
                                  email_dollar_total)
                except FileNotFoundError:
                    print('Workbook does not exist! Check your config file and make sure the workbook exists.')
                    # Create workbook menu function
        except Exception as e:
            print(f'Error in main program during sell logging to excel spreadsheet: {e}')
    else:
        print('Trade logging skipped...')


'''
Take all the options passed on the command line and assign them to their values. Then, once they are in place,
ask the user for each option they did not pass. I will then take that input and make it the value of the option for
the entire click command context. Once the entire click command context is entered, validate the options of the
options that need additional options, and then prompt the user for those too. Once all options that are required
have been entered, list all the options out in a number list and ask for user confirmation. If they say no,
then ask which number from the list they would like to modify and give them a prompt to modify it. After that,
return to the confirmation menu for the user to confirm. If they confirm, pass the final user options dictionary to
the main program and create a timestamped log of the one-liner that would replicate the user input commands they
entered for the trade.
'''


@click.command()
@click.option("--menu",
              type=click.Choice(["menu", "no_menu"]),
              help="Specify whether you are going to use a one liner without the input and settings review menu",
              callback=click_menu,
              default="menu")
# Currently only email based notify, add exchange based trading and atomic wallet GUI manipulation in the future
@click.option("--bot_type",
              type=click.Choice(["notify"]),
              help="Specify the type of bot")
@click.option("--asset",
              type=click.Choice(["bitcoin", "ethereum", "solana", "xrp", "hedera", "cardano", "dogecoin", "shiba-inu"]),
              help="Specify the crypto asset to buy and sell")
@click.option("--capital",
              type=click.Choice(["dollars", "tether", "usdc", "dai"]),
              help="The type of capital you wish to buy the asset with and sell the asset for")
@click.option("--initial_capital",
              type=check_enough_capital,
              help="Specify the initial amount of capital you wish to place your buy order or the amount you used to "
                   "buy the asset you now wish to sell"
              )
@click.option("--start_type",
              type=click.Choice(["buy", "sell"]),
              callback=validate_dependent_options,
              help="The starting order type")
@click.option("--log_trade",
              type=click.Choice(["excel", "false"]),
              help="Specify if you want to log trades to an xlslx spreadsheet to the location you specify in the "
                   "program config file. If 'false' is entered, the trade will not be logged"
              )
# Additional options that could become required
# If starting with sell
@click.option("--sell_order_type",
              required=False,
              type=click.Choice(["basic_sell", "ladder"]),
              callback=validate_dependent_options,
              help="The type of sell order scan type you'd like to  monitor the asset with to alert a sell signal")
@click.option("--asset_bought_price",
              required=False,
              type=float,
              help="If starting with a sell order, the price of the asset you bought it for or what its currently at "
                   "that you want to monitor to compare the future price to"
              )
@click.option("--percent_loss_limit",
              required=False,
              type=check_percentage,
              help="The percent you will allow your initial buy capital to drop by before selling at a loss. Same "
                   "thing as a stop loss percentage."
              )
@click.option("--profit_loss_function",
              required=False,
              type=click.Choice(["profit_harvest", "swing_trade"]),
              callback=validate_dependent_options,
              help="The profit/loss reallocation protocol determining what to do with profits and losses post sell")
# If starting with buy
@click.option("--buy_order_type",
              callback=validate_dependent_options,
              required=False,
              type=click.Choice(["basic_buy", "rsi_buy"]),
              help="The type of buy order scan type you'd like to monitor the asset with to alert a buy signal")
# If basic buy
@click.option("--basic_buy_price",
              required=False,
              type=check_enough_capital,
              help="The price of the asset you want to buy at as an integer or float"
              )
# If RSI buy
@click.option("--rsi_buy_number",
              required=False,
              type=check_percentage,
              help="The RSI you'd like to sell at if it stays at that RSI for the wait period")
@click.option("--rsi_drop_limit",
              required=False,
              type=check_percentage,
              help="The RSI you would not want to drop below after the wait period has expired in the RSI scan")
@click.option("--rsi_wait_period",
              required=False,
              type=check_time_format,
              help="The amount of time to wait before the sell order is placed if an RSI is hit. Format of 00:00:00 "
                   "for hours, minutes, and seconds, minutes and seconds being between 0-59")
# If basic sell
@click.option("--basic_sell_profit",
              required=False,
              type=check_percentage,
              help="The percentage of profit you would like to achieve before the sell signal is true"
              )
# If ladder sell function
@click.option("--minimum_ladder_profit",
              required=False,
              type=check_percentage,
              help="The minimum profit percent gain you want before the sell time begins for the ladder profit sell "
                   "function"
              )
@click.option("--ladder_step_gain",
              required=False,
              type=check_percentage,
              help="The percentage of each step to reset the timer at once the minimum profit has been reached"
              )
@click.option("--ladder_step_loss",
              required=False,
              type=check_percentage,
              help="The percentage drop step that will trigger an immediate sell in the ladder function"
              )
@click.option("--ladder_timer_duration",
              required=False,
              type=check_time_format,
              help="The duration of time to let the price stagnate before you sell. Format of 00:00:00 for hours, "
                   "minutes, and seconds, minutes and seconds being between 0-59"
              )
@click.option("--ladder_step_sensitivity",
              required=False,
              type=float,
              help="The number to divide the step gain and loss percentage to make the number more sensitive the higher"
                   "the profit goes"
              )
@click.option("--ladder_timer_sensitivity",
              required=False,
              type=float,
              help="The number to divide the ladder timer duration by to increase or decrease the time period to sell "
                   "after"
              )
# If profit loss swing trade
@click.option("--swing_trade_skim",
              required=False,
              type=check_percentage,
              help="The percentage of profit you want to skim off to keep and not use to be swing traded."
              )
# History command that reads file output from the command history
@click.option("--history",
              required=False,
              type=click.Choice(["view", "clear"]),
              callback=lof.read_history,
              help="Prints the content of your command history for this program to the terminal.")
def main(**kwargs):
    merge_user_inputs(**kwargs)
    print("\n============================================"
          "\nGathered all user input. Starting program..."
          "\n============================================")
    run_program_procedure()


"""
 For some ridiculous reason, whatever function defined directly after the click options, when the program is called,
 click passes all the values to that function even if you define zero arguments for that function, so this main 
 function takes the click options and command line values pass to click and then passes it to the two functions 
 required for the program
"""


# After the user inputs have been merged, run the program step by step calling the necessary functions
def run_program_procedure():
    """
    Run the main order monitoring procedure step by step based on the order input
    :return:
    """
    """
    1. After gathering and parsing all user input,  create an Order object
    """
    order = create_order_object()

    """
    2. Based on initial buy or sell scan, begin the scan protocol to buy or sell. 
    """
    signal = buy_sell_signal_scan(order)

    """
    3. Once a signal is true, calculate how much to sell with profit/loss function or tell the user to buy now
    and use that information to craft a message for the email notification
    """
    subject, message = None, None
    if signal == 'buy':
        subject, message = buy_signal_email(order)
    elif signal == 'sell':
        subject, message = sell_signal_email(order)

    """
    4. Take the values I want in the message and the put them into an email to notify me
    """
    nof.notify_email(subject, message)

    """
    5. Wait for a response for the email, and if told to wait, wait the specified time. Otherwise, log the trade.
    Will keep checking until the timeout, which the timeout is set in the config file
    """
    email_response = nof.check_email_response()

    """
    6. If an action was taken, log all the info to a spreadsheet and notify the user it completed successfully send
    all the data to the spreadsheet (different logs if bought or sold). otherwise, if the time expired and the 
    email response was none, restart the current order monitoring function
    """
    if email_response is None:
        print("No email response, restarting program scanning!\n")
        run_program_procedure()
    elif email_response:
        log_trade_check(email_response, order)


if __name__ == '__main__':
    try:
        main()
    finally:
        print("\n~~~Bot finished!~~~")
