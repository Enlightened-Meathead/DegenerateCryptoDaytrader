import click

# python3 menu_test.py --bot_type exchange --asset bitcoin --capital dollars --start_type buy --buy_order_type rsi_buy --sell_order_type ladder --percent_loss_limit 10 --profit_loss_function profit_harvest --initial_capital 100
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
'''Once all options have been passed to click, review with the user for confirmation if yes, move on. If no, 
ask the user which one they would like to change. Select that option, then reprompt the user for that option Once all 
options have been gathered by click in either the cli one liner, a cli one liner with missing options corrected by 
the menu, or just the menu, pass them to the main logic module cli one liner with missing options corrected by the 
menu, or just the menu, pass them to the main logic module.'''
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
final_user_options = {"asset": 'bitcoin', 'buy_price': 10, 'sell_price': 100}
click_objects_dict = {}


# If an option is called that needs additional dependencies, add it to the list of missing options
def validate_dependent_options(ctx, param, value):
    global total_missing_options
    missing_options = []
    # Value is the name of the click context value, so that's why I'm using value for the key name
    if value in OPTION_DEPENDENCIES.keys() and ctx.params.get("menu") != "menu":
        for option in OPTION_DEPENDENCIES[value]:
            if option not in ctx.params:
                total_missing_options.append(option)
                missing_options.append(option)
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


# Figure out a way to shrink this function down...
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
def finalize_user_inputs():
    global final_user_options
    global click_objects_dict
    modify_choice_dict = {}
    confirm_choices = 'no'

    while confirm_choices == 'no':
        option_index = []
        print("\n===========================\nYour current option values:\n===========================")
        for key, value in final_user_options.items():
            if value is not None:
                option_index.append(key)
                print(f"{option_index.index(key) + 1}: {key} = {value}")
                modify_choice_dict[option_index.index(key) + 1] = key
        modify_choice = click.prompt("Would you like to modify any option's values?",
                                     type=click.Choice(['yes', 'no']))
        display_options = False
        while modify_choice == 'yes':
            display_options = True
            # Get the length of the index of choices and make it into a list of the range of integers
            choice_length = range(0, len(option_index))
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
                # Convert the choice object into a list to use as the choices for the prompt
                try:
                    choice_list = [choice for choice in change_choices.choices]
                except AttributeError:
                    choice_list = float
                try:
                    changed_option_value = click.prompt(f'Enter new value for {user_option_change}',
                                                        type=click.Choice(choice_list))
                except AttributeError:
                    changed_option_value = click.prompt(f'Enter new value for {user_option_change}',
                                                        type=choice_list)
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
                    print(f"{option_index.index(key) + 1}: {key} = {value}")
                    modify_choice_dict[option_index.index(key) + 1] = key
        confirm_choices = click.prompt("Are these are your final settings? If so, please type CONFIRM and the bot "
                                       "will start. If not, type no to go back and modify",
                                       type=click.Choice(['CONFIRM', 'no']))
        # print a one-liner that the user can copy and paste the next time they want to run this trade as a one-liner


# take the dictionary of the one-liner values and

# I need to take all the options passed on the command line and assign them to their values. Then, once they are in
# place, ask the user for each option they did not pass. I will then take that input and make it the value of the
# option for the entire click command context. Once the entire click command context is entered, validate the options
# of the options that need additional options, and then prompt the user for those too. Once all options that are
# required have been entered, list all the options out in a number list and ask for user confirmation. If they say
# no, then ask which number from the list they would like to modify and give them a prompt to modify it. After that,
# return to the confirmation menu


@click.command()
@click.option("--menu",
              type=click.Choice(["menu", "no_menu"]),
              callback=click_menu,
              default="menu")
@click.option("--bot_type",
              type=click.Choice(["exchange", "atomic", "notify"]),
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
# Possibly refactor the name to stop_loss_limit later
@click.option("--percent_loss_limit",
              type=float,
              help="The percent you will allow your initial buy capital to drop by before selling at a loss"
              )
@click.option("--profit_loss_function",
              type=click.Choice(["profit_harvest", "swing_trade"]),
              callback=validate_dependent_options,
              help="The profit/loss reallocation protocol determining what to do with profits and losses post sell")
@click.option("--initial_capital",
              type=float,
              callback=validate_dependent_options,
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
@click.option("--rsi_drop_limit",
              required=False,
              type=float,
              help="The RSI you would not want to drop below after the wait period has expired in the RSI scan")
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
def merge_user_inputs(**kwargs):
    # take the dictionary of values from menu and compare it to the kwargs and any empty kwargs put the value in it
    global menu_assigned_options
    global final_user_options
    global click_objects_dict
    # Take every click option and make into a nested dictionary to be referenced for outside the scope of the click
    # command
    ctx = click.get_current_context()
    for param in ctx.command.params:
        click_objects_dict[param.name] = param.type

    if ctx.params['menu'] == 'menu':
        # Merge the click command line options with the menu options overwriting the click options
        final_user_options = kwargs | menu_assigned_options
        finalize_user_inputs()

    return final_user_options


if __name__ == '__main__':
    merge_user_inputs()
