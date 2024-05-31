# import logic_functions.profit_loss_functions as plf
import logic_functions.scan_functions as scf

scf.basic_buy_scan("monero", 144.72, 5)
#ladder_sell_scan("bitcoin", 68560, 5, -0.0, 1, -0.5, "00:01:00", 5)
# scf.ladder_sell_scan("bitcoin", 50000, 10, 5, 1, .5, '00:00:10', 5)
# 1. Parse user input to relevant variables

# 2. Based on initial buy or sell scan, begin the scan protocol to buy or sell
# 3. Once a scan protocol has been triggered, initiate the corresponding buy, sell, and/or notify function

# 4. Do the P/LRP
#plf.profit_loss_percent(500)
# 5. If an action was taken, log all the info to a spreadsheet and notify the user it completed successfully
# 6. Based on the outcome of the previous trade, repeat the process with the new numbers

