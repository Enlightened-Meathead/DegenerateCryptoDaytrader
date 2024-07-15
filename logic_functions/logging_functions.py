# Functions that take information from buy and sell orders then log it to a spreadsheet (and/or text document?)
import time
import openpyxl
from openpyxl import Workbook, load_workbook

"""
 Values to append:order_timestamp, asset, buy_price, asset_amount_bought, dollar_amount_bought,
 sell_timestamp, sold_price, asset_amount_sold, profit_loss_percent, asset_profit_loss, dollar_profit_loss 
"""


# total losses=SUMIF(K2:K999, "<0")
# total profits=SUMIF(K2:K999, ">0")
# net=SUM(K2:K999)


# If you manually create a workbook in Excel or in my case LibreOffice Calc beforehand, you'll have issues with openpyxl
def create_initial_workbook():
    workbook = Workbook()
    sheet = workbook.active
    headers = ["Order Number", "Date and Time", "Asset", "Bought Price", "Asset Amount Bought", "$ Amount Bought",
               "Sold Price", "Amount of Asset Sold", "Profit/Loss %", "Profit/Loss $ Amount", "$ Total Losses",
               "$ Total Profits", "$ Total Net"]
    sheet.append(headers)
    workbook.save("../resources/trade_log.xlsx")


# trade and append it to the trade_log spreadsheet
def log_trade(*args):
    # Load in the workbook and select the main sheet then find the current free row
    #try:
    workbook = load_workbook("../resources/trade_log.xlsx")
    sheet = workbook.active
    next_row = sheet.max_row + 1
    print(next_row)
    order_number = sheet.max_row - 1
    print(order_number)
    # Create a list of values to be appended from arguments passed to the function
    values_to_append = list(args)
    values_to_append = [order_number] + values_to_append
    print(values_to_append)

    # Add each value to their cells
    for column, value in enumerate(values_to_append, start=1):
        sheet.cell(row=next_row, column=column, value=value)
        print(f"Writing to row: {next_row}, column: {column}, value: {value}")
    # Save the changes to the spreadsheet
    try:
        workbook.save('../resources/trade_log.xlsx')
        workbook.close()
    except Exception as e:
        print(f"Error in log_trade trying to save to workbook: {e}")


#except Exception as e:
#print(f"Error in log_trade trying to open workbook: {e}")


if __name__ == "__main__":
    log_trade("buy timestamp", 'asset test', 'buy price', 'amount bought', 'dollar amount bought', "sold price",
              "amount sold", "profit %",
              "asset pl", "+20")
    #pass
