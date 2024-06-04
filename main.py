import logic_functions.scan_functions as scf
import logic_functions.notify_functions as nof
import logic_functions.profit_loss_functions as plf
import logic_functions.logging_functions as lof

# Could possible have the cli_menu run this below as with main_program_procedure(merge_user_inputs())


#scf.basic_buy_scan("monero", 144.72, 5)
#ladder_sell_scan("bitcoin", 68560, 5, -0.0, 1, -0.5, "00:01:00", 5)
# scf.ladder_sell_scan("bitcoin", 50000, 10, 5, 1, .5, '00:00:10', 5)

# 1. Parse user input to relevant variables
# Use the cli_menu file to get this dictionary of user input
test_user_options = {'bot_type': 'notify', 'percent_loss_limit': '2', 'basic_buy_price': '100', 'buy_order_type': 'basic_buy', 'basic_sell_profit': '5', 'asset': 'bitcoin', 'capital': 'dollars', 'start_type': 'buy', 'sell_order_type': 'basic_sell', 'profit_loss_function': 'profit_harvest', 'menu': 'menu', 'initial_capital': '100', 'rsi_buy_number': None, 'rsi_drop_limit': None, 'rsi_wait_period': None, 'minimum_ladder_profit': None, 'ladder_step_gain': None, 'ladder_step_loss': None, 'ladder_timer_duration': None, 'ladder_step_sensitivity': None, 'ladder_timer_sensitivity': None, 'swing_trade_skim': None, 'history': None}

# 2. Based on initial buy or sell scan, begin the scan protocol to buy or sell
def main_program_procedure(final_user_options):
    # Start a buy scan if the start_type is buy
    if final_user_options['start_type'] == 'buy':
        if final_user_options['buy_order_type'] == 'basic_buy':
            pass
        elif final_user_options['buy_order_type'] == 'rsi_buy':
            pass
    elif final_user_options['start_type'] == 'sell':
        if final_user_options['sell_order_type'] == 'basic_sell':
            pass
        if final_user_options['sell_order_type'] == 'ladder':
            pass

# 3. Once a buy or sell signal is true, take the values and calculate how much to buy or sell with plrp
# 4. Take the values I want in the message and the put them into an email to notify me
# 5. Wait for a response for the email, and if told to wait, wait the specified time. Otherwise, log the trade
# 6. If an action was taken, log all the info to a spreadsheet and notify the user it completed successfully

# 7. Based on the outcome of the previous trade, take the values that would change for the new trade and change those
# in the user options dictionary

# 8. repeat the process with the new numbers

