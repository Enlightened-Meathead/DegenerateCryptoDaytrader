from datetime import datetime
import re
import click
import asyncio

import logic_functions.scan_functions as scf
import logic_functions.notify_functions as nof
import logic_functions.profit_loss_functions as plf
import logic_functions.logging_functions as lof

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
    'swing_trade': ['swing_trade_skim']
}
REQUIRED_OPTIONS = ['bot_type', 'asset', 'capital', 'start_type', 'buy_order_type', 'sell_order_type',
                    'percent_loss_limit', 'profit_loss_function', 'initial_capital']

total_missing_options = []
menu_assigned_options = {}
final_user_options = {}
selected_user_options = {}
click_objects_dict = {}


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


'''- for the menu, for every option, create a prompt with the message being the help message, the click choices the 
prompt choice, then make the answer to that prompt equal to the parameter value for that parameters name then pass 
that option to click. If the program is called with menu and some options, start the menu but only for their missing 
options - say the user is missing some options, and tell them if they dont want this menu pass the argument no menu - 
check if the passed options require optional dependencies. for every global total missing option, prompt the user to 
enter them'''


# IF YOU ENTER THE MENU OPTION AS THE FIRST OPTION PASSED, NO ARGUMENTS GET PASSED TO CLICK
# Figure out a way to shrink this function down in the future.
# Click CLI menu
def click_menu(ctx, param, value):
    global REQUIRED_OPTIONS
    global OPTION_DEPENDENCIES
    global total_missing_options
    global menu_assigned_options
    make_required(ctx, param, value)
    if value == 'menu':
        click.echo(menu_banner)
        for option in ctx.command.params:
            # For every option in the click command that hasn't been given a value on the command line and is required:
            if option.name not in ctx.params.keys() and option.name in REQUIRED_OPTIONS:
                user_input = click.prompt(f"{option.help}", type=option.type)
                # If the user input has associated dependencies
                if user_input in OPTION_DEPENDENCIES.keys():
                    # For every dependency for the user input option
                    for option_dependency in OPTION_DEPENDENCIES[user_input]:
                        # Check if the dependency was passed at the command line, if not, prompt the user to add it.
                        if option_dependency not in ctx.params.keys():
                            dependency_option = next(
                                (opt for opt in ctx.command.params if opt.name == option_dependency), None)
                            dependency_user_input = click.prompt(f"{dependency_option.help}",
                                                                 type=dependency_option.type)
                            menu_assigned_options[dependency_option.name] = dependency_user_input
                menu_assigned_options[option.name] = user_input
        # If any missing options exist from the command line, prompt the user for those as well
        click.echo("The following are required additional options based on some of your options you passed on the "
                   "command line:")
        # For the missing options that weren't passed at the command line with the option that requires them
        for option in total_missing_options:
            # Get the option object that was missing from the command line and prompt the user
            dependency_option = next(
                (opt for opt in ctx.command.params if opt.name == option), None)
            dependency_user_input = click.prompt(f"{dependency_option.help}",
                                                 type=dependency_option.type)
            menu_assigned_options[dependency_option.name] = dependency_user_input
    return value


# Check if the user input is an integer or the string 'cancel' to escape the modify loop
def integer_or_cancel(user_input):
    try:
        return int(user_input)
    except ValueError:
        if user_input == "cancel":
            return user_input


# Could definitely be optimized, but for now its functional
"""This big kahuna is a user review menu that takes the user inputs from the command line and menu then lets them 
review them and update them. Once the user confirms their final settings, it takes all the user inputs and converts 
them to a one-liner they can copy paste if they want to run the same trade and stores it into a command history log 
file for this program. The reason this function is so massive is because I was struggling to pass the click context 
to multiple functions without issues so here we are for now with this abomination"""


def finalize_user_inputs():
    global final_user_options
    global click_objects_dict
    global selected_user_options
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
                    #if type(choice_list) == list:
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
    if 100 >= float(input_value) > 0:
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


# Print a one-liner that the user can copy and paste the next time they want to run this trade as a one-liner
def repeat_one_liner():
    global selected_user_options
    # Make this a config setting that lets the user save what they have their alias to the log file
    program_alias = "degenerate_crypto_daytrader"
    command_option_list = []
    print("\n===========================\nCurrent Options One-Liner:\n===========================")
    # Add the --option value strings to a list then join the list
    for option, value in selected_user_options.items():
        command_option_list.append(f"--{option} {value}")
    command_option_string = ' '.join([string for string in command_option_list])
    current_one_liner = f'python3 {program_alias} {command_option_string}'
    print(current_one_liner)
    # Get a timestamp and write the command to the history log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('./resources/dcd_command_history.txt', 'a') as history:
        history.write(f'\n{timestamp} : {current_one_liner}')
    # Add in a ring buffer size to the history log file
    # Man page entry for this function


# Read the command history log file
def read_history(ctx, param, value):
    if value == "view":
        with open('resources/dcd_command_history.txt', 'r') as history:
            print(history.read())
            exit()
    elif value == "clear":
        # Open the file with write, which clears the contents of the file
        with open('./resources/dcd_command_history.txt', 'w') as history:
            exit()


"""Here is a one-liner of your settings for this trade; if you wish to make " "this exact trade again," "you can copy 
this command to save somewhere and/or alias it along with different trades you plan on making " "on a frequent basis. 
This command will be saved to the 'dcd_command_history.txt' in this programs directory. " "Besides manually reading 
this file, if you would like to print your previous commands, run this program " "with the --history option."""


# Take all the options passed on the command line and assign them to their values. Then, once they are in place,
# ask the user for each option they did not pass. I will then take that input and make it the value of the option for
# the entire click command context. Once the entire click command context is entered, validate the options of the
# options that need additional options, and then prompt the user for those too. Once all options that are required
# have been entered, list all the options out in a number list and ask for user confirmation. If they say no,
# then ask which number from the list they would like to modify and give them a prompt to modify it. After that,
# return to the confirmation menu for the user to confirm. If they confirm, pass the final user options dictionary to
# the main program and create a timestamped log of the one-liner that would replicate the user input commands they
# entered for the trade.


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
              type=click.Choice(["bitcoin", "ethereum", "solana", "xrp", "cardano", "dogecoin", "shiba-inu", "monero"]),
              help="Specify the crypto asset to buy and sell")
@click.option("--capital",
              type=click.Choice(["dollars", "tether", "usdc", "dai"]),
              help="The type of capital you wish to buy the asset with and sell the asset for")
@click.option("--start_type",
              type=click.Choice(["buy", "sell", "previous"]),
              help="The starting order type")
@click.option("--buy_order_type",
              type=click.Choice(["basic_buy", "rsi_buy"]),
              callback=validate_dependent_options,
              help="The type of buy order scan type you'd like to monitor the asset with to alert a buy signal")
@click.option("--sell_order_type",
              type=click.Choice(["basic_sell", "ladder"]),
              callback=validate_dependent_options,
              help="The type of sell order scan type you'd like to  monitor the asset with to alert a sell signal")
@click.option("--percent_loss_limit",
              type=check_percentage,
              help="The percent you will allow your initial buy capital to drop by before selling at a loss. Same "
                   "thing as a stop loss percentage."
              )
@click.option("--profit_loss_function",
              type=click.Choice(["profit_harvest", "swing_trade"]),
              callback=validate_dependent_options,
              help="The profit/loss reallocation protocol determining what to do with profits and losses post sell")
@click.option("--initial_capital",
              type=check_enough_capital,
              callback=validate_dependent_options,
              help="Specify the initial amount of capital you wish to place your buy order"
              )
# Additional options that could become required
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
              callback=read_history,
              help="Prints the content of your command history for this program to the terminal.")
def main(**kwargs):
    merge_user_inputs(**kwargs)
    run_program_procedure()


"""
 For some ridiculous reason, whatever function defined directly after the click options, when the program is called,
 click passes all the values to that function even if you define zero arguments for that function, so this main 
 function takes the click options and command line values pass to click and then passes it to the two functions 
 required for the program
"""


def merge_user_inputs(**kwargs):
    global menu_assigned_options
    global final_user_options
    global click_objects_dict

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
        repeat_one_liner()
    print(f"\n{final_user_options}")


'''
 This file is way too long as it is, but after writing all this I learned it would be pretty difficult to run click
 in a different file and pass the final user options to the file, so I'm just writing it in here for now to get it
 WORKING and if I have time in the future to nitpick and divide this file up, I will
'''


def run_program_procedure():
    global final_user_options
    print("Gathered all user input. Starting program...")
    buy_signal = False
    sell_signal = False
    amount_to_buy = 0
    asset_bought_price = 0
    amount_to_sell = 0
    amount_to_keep = 0
    asset_sold_price = 0
    # 2. Based on initial buy or sell scan, begin the scan protocol to buy or sell. Also, rescan if the user doesn't
    # reply in a certain amount of time or the user says to cancel and restart the scan
    print(final_user_options['start_type'])
    if final_user_options['start_type'] == 'buy':
        if final_user_options['buy_order_type'] == 'basic_buy':
            buy_signal = scf.basic_buy_scan(final_user_options['asset'],
                                            final_user_options['basic_buy_price'],
                                            5)
        elif final_user_options['buy_order_type'] == 'rsi_buy':
            buy_signal = scf.rsi_buy_scan(final_user_options['asset'],
                                          final_user_options['rsi_buy_number'],
                                          final_user_options['rsi_drop_limit'],
                                          final_user_options['rsi_wait_period'])
    elif final_user_options['start_type'] == 'sell':
        if final_user_options['sell_order_type'] == 'basic_sell':
            sell_signal = scf.basic_sell_scan(final_user_options['asset'],
                                              asset_bought_price,
                                              final_user_options['basic_sell_profit'],
                                              final_user_options['percent_loss_limit'])
        if final_user_options['sell_order_type'] == 'ladder':
            sell_signal = scf.ladder_sell_scan(final_user_options['asset'],
                                               asset_bought_price,
                                               final_user_options['minimum_ladder_profit'],
                                               final_user_options['percent_loss_limit'],
                                               final_user_options['ladder_step_gain'],
                                               final_user_options['ladder_step_loss'],
                                               final_user_options['ladder_timer_duration'],
                                               final_user_options['ladder_step_sensitivity'],
                                               final_user_options['ladder_timer_sensitivity'])
    else:
        print("The program was unable to determine a buy or sell to start the trade. ABORTING!")
        exit()
    # 3. Once a buy or sell signal is true, calculate how much to sell with plrp or tell the user to buy now
    subject = ''
    message = ''
    if buy_signal:
        print("Buy signal found!")
        asset_bought_price = float(asyncio.run(scf.current_price_scan(final_user_options['asset'])))
        amount_to_buy = float(final_user_options['initial_capital']) / asset_bought_price
        subject = 'DCDB'
        message = (f"Buy {amount_to_buy} {final_user_options['asset']} at the current price of {asset_bought_price} at "
                   f"the time of this email")
    elif sell_signal:
        print("Sell signal found!")
        amount_bought = final_user_options['initial_capital'] / asset_bought_price
        profit_loss = plf.profit_loss_percent(final_user_options['asset'], asset_bought_price)
        if final_user_options['profit_loss_function'] == 'profit_harvest':
            # add in a user click option if they want a full sell for the profit harvest
            amount_to_sell = plf.profit_harvest(asset_bought_price, amount_bought)
        elif final_user_options['profit_loss_function'] == 'swing_trade':
            amount_to_sell = final_user_options['initial_capital'] / scf.current_price_scan(final_user_options['asset'])
            next_buy_amount = plf.swing_trade(amount_bought, amount_to_sell, final_user_options['swing_trade_skim'])
        asset_sold_price = scf.current_price_scan(final_user_options['asset'])
        subject = 'DCDS'
        message = (f"Sell {amount_to_sell} from your {amount_bought} {final_user_options['asset']} according to your "
                   f"selected {final_user_options['profit_loss_function']} profit loss function for a current {profit_loss}")
    else:
        print("The buy and sell signal checks ended, but somehow none were set to true. ABORTING!")
    # 4. Take the values I want in the message and the put them into an email to notify me
    nof.notify_email(subject, message)


# 5. Wait for a response for the email, and if told to wait, wait the specified time. Otherwise, log the trade
# 6. If an action was taken, log all the info to a spreadsheet and notify the user it completed successfully

# 7. Based on the outcome of the previous trade, take the values that would change for the new trade and change those
# in the user options dictionary

# 8. repeat the process with the new numbers


'''
barebones notify version now ready for testing, once this works, add all the stuff below here
'''

if __name__ == '__main__':
    main()
