### Degenerate Crypto Daytrader
This readme is a rough scratchpad until the program is working, so grammar and readability to the wind
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

~~ccxt: library that allows me to do trades on exchanges!!!!!!!~~ Turned out to be a bust, API key restrictions are meh
  - use initially to just get prices, see if you can then use ccxt for the buy and sell function on and exchange, then make a gui interface app so use a no kyc dekstop wallet like atomic
- rsi scan interface

#### CLI interface and help/man pages
- create a function that checks for a key value passed to any option that triggers additional options and if found, set the corresponind option requirement to true
- test and make sure if a one liner is done, the values are stored in the correct place and a dictionary of the values is created
- for every option, create a check and logic that makes sure every value is the correct data type and within the specifiecd range
- use regex to make sure the time format is correct and make the minutes and second 0-59
- once the command line one-liners are functional, convert it to an interactive menu that gets all the required info
- review page at the end of the menu that gives an option to edit any of the values
- confirm the values for one liners or menu
- have an option for one liners to force start and skip confirmation
- GUI menu? yeah probably a good idea, do way later once everything is functional and working together
- man page that deeply explains all options, also explains all functions and how they work as well as general guidance for noobs, do this later once everything works

End goal is have a one liner or cli menu that confirms the user input then passes that input to the main function
- 


End goal is have a one liner or cli menu that confirms the user input then passes that input to the main functio
posssibly add modules for leveraged trading?

### Completed
- basic buy and rsi based buy logic scan functions
- basic sell and ladder ascending profit logic scan functions
- profit loss allocators that tell what to buy back in with if swing trading and what to sell if profit harvesting
- web socket based price scanner that returns the current spot price every 5 seconds for the selected asset.
- 