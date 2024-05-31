# Functions that take information from buy and sell orders then log it to a spreadsheet (and/or text document?)
import time
import openpyxl
from openpyxl import Workbook, load_workbook


# Values to append: order_number, buy_timestamp, asset, buy_price, asset_amount_bought, dollar_amount_bought,
# sell_timestamp, sold_price, asset_amount_sold, profit_loss_percent, asset_profit_loss, dollar_profit_loss Take
# values from the

# trade and append it to the trade_log spreadsheet
def log_trade(*args):
    # Load in the workbook and select the main sheet then find the current free row
    workbook = load_workbook("../resources/trade_log.xlsx")
    sheet = workbook.active
    next_row = sheet.max_row + 1
    order_number = sheet.max_row - 1

    # Create a list of values to be appended from arguments passed to the function
    values_to_append = list(args)
    values_to_append = [order_number] + values_to_append

    # Add each value to their cells
    for column, value in enumerate(values_to_append, start=1):
        sheet.cell(row=next_row, column=column, value=value)
    # Save the changes to the spreadsheet
    workbook.save('test.xslx')
