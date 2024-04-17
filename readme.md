### Degenerate Crypto Daytrader

Intentions:
- CLI based python app that you give user input to what crypto to buy and trade with given trade parameters and buy and sell protocols using a centralized exchange to do the trades then logsn and record the data of the trade for tax purposes
- This is my first real programming project, so mainly the goal is to learn and just do even if something isn't optimal. If something isn't perfect, I don't care. I'm learning, and doing is better than doing nothing because I'm being neurotic about perfection 

To Do:
- user login method for the wallet or exchange to user
- ask the user their preferences with a cli based menu
- Scan function that scans a website that gives data on the price/
- Buy function that with given parameters will buy a set amount you give the program
- Sell function that follows sell protocols given by the user
- Profit/loss reallocation protocol functions that once a sell order is initiated, determine what to do with the profit or loss for the next buy order
- sms or email or both server that asks for verification before any buy or sell order
- logging system that logs all the data to a spreadsheet that includes the date bought and sold, price bought and sold old, profit or loss percent and value
- a way to interface with on desktop wallets that are gui based or websites to allow automated trading

First Steps:
- user menu selecting the following info:
  - What currency are you buying
  - What buy order function?
  - what buy order conditional close?
  - what sell order function?
  - what sell order conditional close?
  - profit loss reallocation function

- Function protocols for buying and selling, the logic engine basically 
  - buy protocol functions
  - sell protocol functions
  - profit loss reallocation function
  - testing function with spoof numbers given by the user to test how the program works 
