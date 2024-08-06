# Degenerate Crypto Daytrader
___
## 🎯 What Is This Program For?
- This project is a day-trading bot that is meant to take out all the labor and thinking of being a degenerate who day-trades crypto. It requires no API keys for the end user to get, and you can use NoKYC wallets and DEXes or any exchange with this program. This program currently DOES NOT automatically buy or sell anything by itself; it just tells you exactly how much to buy and sell and when exactly to do so. It is a command-line application written in Python 3. It's function is to take the user input on a trade/order position they have open or wish to open as defined as a buy or sell order, and then, based on that user input, monitor price and technical indicator data and process that data with custom algorithms until a sell or buy signal the user desires is reached. Upon reaching that signal, the bot will send a desktop notification and/or email to the user (optionally GPG encrypted) and then wait for a user response either through the user typing data back into the terminal or parsing simple commands and data the user can send the bot from any email. Once the commands/data have been received, the bot responds accordingly and will either wait for a specified time and re-scan for a buy/sell signal or take the user-specified data of the order they made and log it to an Excel spreadsheet. This is my first ever piece of programming/software, so I was learning how to code and do everything along the way. The result is something that seems good to me, but obviously the first thing any programmer writes is probably garbage, and I am most likely no exception. However, the program works perfectly for what I set out for it to do, and from my personal testing across Linux and Windows using a pip virtual environment, it works just fine. Any and all feedback is appreciated :)

---
# 📦 Install ↓ 
This program is designed to currently be completely self-contained in the project directory you download from this GitHub page. If there is enough interest from people, I may package it nicer and also host it in the AUR. The config file, the command and message histories, and the trade log are all found in the 'resources' directory. 

- You can choose to install the libraries required for this program system-wide or in a virtual environment. This guide shows how to do both. 

### Clone the Repo

```bash

# Navigate to where you want this program installed, then:

git clone https://github.com/Enlightened-Meathead/DegenerateCryptoDaytrader

cd DegenerateCryptoDaytrader

```

#### Required External Libraries:

click : used for the CLI menu

openpyxl : used for excel logging

plyer : used for desktop notifications

python_gnupg : used for GPG email encryption

selenium : used for the RSI scan

websockets : used for various websocket connections made in the program

For installing these libraries:

##### System Wide

```bash

cd /path/to/this/programs/directory

pip install -r requirements.txt

```

##### Virtual Environment 

```bash

cd /path/to/this/programs/directory

python -m venv .venv

# On Windows

.venv\Scripts\activate

# On Mac/Linux

source .venv/bin/activate

pip install -r requirements.txt

# After you are done and want to go back to the system wide environment in the terminal, you can close the terminal or just deactivate the virtual environment

deactivate

```

### Quick start

- If the repo is cloned and the dependencies are installed, try running the program by itself to see the menu:

```bash

python3 degenerate_crypto_daytrader.py

```

    - use a chmod +x on the degenerate_crypto_daytrader.py file if you want to just be able to use ./ instead of python3

- To do a quick test, enter the one-liner command below that should send you a desktop notification to buy $100 worth of bitcoin if the price is less than $100,000:

```bash

python3 degenerate_crypto_daytrader.py --basic_buy_price 100_000 --buy_order_type basic_buy --log_trade false --start_type buy --initial_capital 100 --asset bitcoin --bot_type desktop_notify --menu menu

```

---

## 1️⃣ In Depth Intro  

* This program is launched from a terminal using your Python 3 interpreter. From the install steps above, you can launch the program as a script or preface it with 'python' for Windows or 'python3' for Linux to start the program's user menu. If you start the program with no options or arguments passed, you will be presented with a menu to enter the options you'd like to use for the bot.
1. After starting this program for the first time, a config file named 'config.py' now exists within the program's 'resources' directory. If you want to use email notifications, log your trades with Excel, or change the one liner history alias, take a look at the file and change what needs to be changed. Instructions for each configuration exist within the file itself, or just take a look at the 'default_config.py' in this GitHub repo in the same 'resources' folder.

![[starting.png]]
    2. Once the config file exists, the program will print a banner and have a series of prompts that you can enter what you want the bot to do. The format is the help page info, then in brackets the options you can exactly type to enter for that option. While most of these options should be self-explanatory, make sure you fully understand what each option does so you don't configure the bot to monitor incorrectly from what you want. You can read what the options are using the --help option after the command or read the in-depth descriptions of the options below in the docs.

![[step2.png]]
    3. If you have filled out the necessary options the program asks for, you will then be presented with a confirmation menu. If you want to change any option values you have entered, you can type 'yes' and the menu will ask for the index of what option you would like to change. In the example below, I select '3' to change the asset to be looked for to buy, and then change the price to look for in the scan accordingly as well. 

![[step3.png]]
    4. Once you are sure the options you want are correct, you type 'CONFIRM' and the program will begin.
    5. You may think, gee, that was a lot of typing for one monitoring command! You're right, and that's why there is output of 'Current Options One-Liner' that can be seen in the example above, as well as a history option for this command. If you want to modify or reuse this scan, you can simply copy and paste the full one-liner into the terminal, and all your options are automatically entered into the menu, and then you can just confirm to start the order or modify just what you want rather than retyping things that would be redundant. If you cleared your terminal or the command was run way up in your terminal history, you can use the --history option to get a list of all the output of previously ran commands as one liners. More information on the history option is below in the option guide.

![[step4 1.png]]
    6. Besides using the menu to enter the options you want and the --history option, you can also type out options directly to the command line with the '--option value' syntax. If you do this, some options require dependent options, such as if you specify the '--order buy' option, you then need to specify which type of buy order scan you would like done, such as '--buy_order_type basic_buy'. Typing full one liners is quite verbose, and generally you would want to use the menu at first unless you become extremely familiar with the program, but if you do want to pass everything as a one liner, you need to know that the Click library, which is used to help collect the options passed at the command line, reads the options from the front of the command to the end, and if you put a parent option before a dependent option, the program will throw an error and trigger the menu for you to manually input the missing option. This is a fault of the Click library and my lack of knowledge initially of how it worked, but if you use the command logged one-liners from the history file or menu output, this problem is solved and all the options are in the correct order to do a one-liner. If you want to skip the menu confirmation and just start the scan, you can pass the '--menu no_menu' option at the end of the one liner for it to skip confirmation. This is useful if you want to alias the command to automatically start buy order scans based on RSI technical indicators instead of changing metrics like price.
    7. Once the scan begins, sit back and wait for your notification and/or email. If you didn't modify the config file and setup email, you can just use the bot as a desktop notifier. In KDE Plasma, you can push desktop notifications to your phone with KDE Connect, so even if you don't want to setup email use for notifications, you can still get notifications to your phone if you're using an OS and programs that support pushed notifications to mobile from your desktop. For a desktop notifier, if you decide to log the trade to a spreadsheet, you can go to the terminal and enter the info it asks of you. For buy and sell orders, it will ask for the dollar amount you bought/sold and the asset amount you bought/sold. If you want to command the bot to wait for a certain period of time and after that time expires restart the scan, you can do that as well. Just press enter for the values that you don't want to pass any values to, so if you log the trade saying you bought $100 of HBAR and that resulted in 1428.57 HBAR tokens, you enter those values, and when you are presented with if you want to instruct the bot to wait, just press enter.

![[step5.png]]
    8. In this case, we logged the trade to the spreadsheet, which can be found in the 'resources' directory and is named 'trade_log.xlsx'. If you don't have a trade log created, the first time the program tries to append the trade to the log, it will prompt you with a menu to create one.
    9. Once a trade log exists, any future completed scans will be appended to that log file. If you want to delete the trade log spreadsheet, manually delete it from the 'resouces' directory.

---
# 📃THE DOCS   
### General Tips and Knowledge  
- If you want to use email for notifications and remote commands, read the config file! If you are going to use email, you at a minimum need a separate throwaway gmail you want to use to be the bot's email.

- There are four total scan types: basic_buy, rsi_buy, basic_sell, and ladder. If you want to start easy, just use basic_buy and basic_sell. These scans just identify a price you specify as a trigger point to alert you. For example, if you want to scan for when bitcoin dips below $60k, you can use basic_buy as the buy_order_type and use 60_000 (or 60000, Python parses the underscores out of numbers) for the basic_buy_price, and this will say to the bot, 'Okay, go out there and scan bitcoin for me, and when it hits or dips below $60k, alert me that I should buy'. This works the opposite of sell, but with the same premise. If the basic_sell_percent is 5% when you scan, it will alert you when the price of bitcoin rises above the price you bought it for if the current price is 5% higher.

- The program is fairly light on resources, as the price scan is just connecting to a public websocket once and maintaining that connection and just doing some basic arithmetic locally with that data, pushing a notification and/or a single email, and then monitoring for user input to the email inbox or just the terminal input until it finally finished logging everything to a spreadsheet. The only thing that takes a little more resources is the RSI buy scan, which opens a Firefox browser using Selenium to be able to grab dynamic JavaScript page data and parse that information to get the current RSI, but this isn't too resource heavy. Basically, the point I'm getting at is that this is something you can run in the background on your main PC or on a server and even have multiple instances running of multiple trades, and it won't hog your resources.  

- Everything in this program is self-contained in the directory you downloaded the program in. The config file, history files, trade log, and script all exist locally in that self-contained directory. That is by design for now, as this is a first release still, and if it ever grew to where I thought it would be worth creating an installer, I may in the future. For now, it's self-contained. If you want to be able to run it from anywhere in the terminal, just add it to your shell config file as an alias or put it in a directory that is part of your path (make sure you fully know what the hell you are doing if you try and add this to your path). 

- The email commands are sent back in key-value pairs separated by a comma. In the config file, you can specify what key you would like by changing the keys of the 'user_response_keys' dictionary. For example, t is the dollar value amount for the final price of the trade after fees, so if the total traded was $103.67 and the total asset amount bought was 10.3, you would compose a new email to the bot's email, enter the subject name 'DCD' by default (or whatever you want it to be, you can set in the config file), then in the email message you can enter t:103.67,a:10.3 and the bot will parse this and use it for logging to the spreadsheet. If you have logging set to false and not 'excel', then the program will just notify you and end as the scan is complete and it requires no further user input.
## 🔰 Command Option Overview
Syntax: program_name --option1 value1 --option2 value2


For each option below, the option is defined, and the values are square brackets separated by | pipes. The program name you call by default is 'degenerate_crypto_daytrader', but feel free to alias it to something else shorter. For the purpose of this guide, the program name will be referred to as 'DCD'. All options that require a single number can use underscores to separate groups of three digits, such as using 100_000 instead of 100000.

--help : Prints a basic help page to refresh you on whats what. Not as in depth as this command option help page below.

--history [view|clear] : This option will print all the commands you have run as one-liners of the final command you passed to DCD. You can then copy and paste these commands and run them again, modifying accordingly. The 'clear' value clears the entire command history file and makes it empty. This command history file can be found in dcd_command_history.txt inside the 'resources' directory, and if you delete the file, DCD will create one as soon as the next message is created.

--message_history [view|clear] : This option with 'view' will print the contents of DCD's notification and email history. If you missed a notification on your desktop or, for whatever reason, couldn't get access to the recipient's email the message was sent to, you can use this to see the missed message. The 'clear' value clears the entire message history file and makes it empty. The message history file can be found in dcd_message_history.txt, and if you delete the file, DCD will create one as soon as the next message is created.

--menu [menu|no_menu] : The menu option is passed by default to DCD. When the menu option is passed, DCD reads all options from left to right and does the callback command for each option. If you enter the --menu option before any other option, all other options will not be read and ignored because the menu will start. Since the menu is called by default, you do not need to manually write out this option. If you are doing a one-liner and want to skip the confirmation menu, you can explicitly call the menu option with the 'no_menu' value. This will parse your command for correct syntax, and if it finds an error or a missing dependent option that needs to be called that you missed, a clear output will be given saying you are missing the following xyz options; enter them and run the program again instead of finding the missing options and letting you enter them in the CLI menu. 

--bot_type [desktop_notify|email_notify] : The type of bot you would like DCD to operate as. The 'desktop_notify' option will push a desktop notification of when to buy or sell based on your input. The amount of time the notification exists on the desktop is set in the config file, defined in seconds. By default, the notification length is set to 3000 seconds, so you probably won't miss it. If you ever do miss a notification, you can use the above '--message_history view' option to print all previous notification messages and emails to the terminal. These are dated and timestamped, so you should easily be able to figure out what's what.   
    - The 'email_notify' option makes the bot send a desktop notification AND an email to the'recipient_email' you define in the config file. More information about how to set up your recipient email is in the config file. Quick summary though: you should be able to use any email client as the receiver, and receiver emails also support GPG encryption before the message leaves your system. The reason GPG encryption is done locally even though the connection is TLS to the email server is so Google (I only tested and used Gmail as the sender) can't be its nosy little self. For the sender email, I recommend you use a throwaway gmail account that will only be used for this program.

--asset [bitcoin|ethereum|solana|xrp|hedera|cardano|dogecoin|shiba-inu] : The asset you are using for the trade. If you are doing a buy order, you will be monitoring the asset you choose for when you want to buy it based on price or RSI. If you are selling the asset you select, you will be monitoring for an increase in price from when you bought it in percentages gained or lost.

--capital [dollars|tether|usdc|dai] : For now, just select dollars. In the future, when and if I automate the trades themselves, then you will have to select what capital you wish to use.

--initial_capital [float or int] : The dollar amount of your position if it is a sell or the dollar amount you wish to use for buying your buy position.

--start_type [buy|sell] : The type of order the bot will start with.

--log_trade [excel|false] : The type of logging of the trade you would like to do. If you don't want the information of the trade logged to a local spreadsheet that exists in the resources folder by default (you can change this in the config file), then simply enter false. If you do want to log the trade to an Excel workbook, then enter 'excel'. If you do log the trade, you will need to enter the total dollar amount after fees bought/sold as well as the total asset amount bought/sold. You can enter these amounts in the terminal you ran DCD if it's a desktop_notify for the bot type, or you must email the bot back with a new message, not a reply, with the subject 'DCD' and the message being the key value pair of the dollar total and asset amount. By default, the dollar amount key is 't' for total and 'a' for the asset amount. So in the message of the email, if you bought 0.1 Bitcoin for $6,000, your email message back would be 't:6000,a:0.1'. You can change these key values in the config file, and the email response parser is fairly robust, so if you add a space after the comma that is used to separate values, that's fine too. But the basic response syntax is 'key:value,key:value', a colon separates the keys and values, and each value/command is separated by a comma.

### Everything above this line is a required option for DCD to run; everything below may become required if its parent option is selected.

### Buy Orders  
--buy_order_type [basic_buy|rsi_buy] : If you selected the bot to start with a buy, then you need to select the buy order type. The basic buy just scans for a specific dollar value price to alert you for. The RSI buy scan scans the technical indicator relative strength index (RSI) and signals to buy when the RSI drops to within a range you specify. If you don't know what RSI is, go look it up. If you just want to use a basic scan for say dollar cost averaging more efficiently, then you can use the basic_buy to scan for dips to pick up.

--basic_buy_price [Float or int] : The price of the asset you wish to buy at. If you want to buy Bitcoin when it drops to or below $60,000, you can set this to '60_000'.

##### RSI Buy Dependent Options  
- The RSI buy scan works by using Selenium and Firefox to scan for the RSI of the asset you picked for DCD. It will open a browser controlled by the bot and may require you as a user to click through some cloudflare/CAPTCHA stuff if it deems you fishy. I modified the user agent info of the bot when it sends the request, so I haven't had to do any user input on the page, but just double check that the browser lands on the page when the scan starts. The page then once again just scrapes the dynamic javascript on the page for the changing RSI. 

--rsi_buy_number [Float or int] : The RSI you'd like to buy once it reaches or drops below this number. RSI is numbered 0-100. The recommended common number is 30, but do your research and feel out the market for what you think is a good number at that time. Once this number is hit, the wait period will start.

--rsi_drop_limit [Float or int] : The RSI you don't want to drop below to if you run the RSI buy scan. This is so you don't buy immediately when a low RSI is reached, and instead of catching the dip, you catch the start of a massive short-term drop. If you set this to 20, then if the RSI set above is 30, as long as the RSI remains in the range of 30-20 for your RSI timer value, then you will get a buy signal.

--rsi_wait_period [hours:minutes:seconds] : The amount of time you want the RSI to wait once the rsi_buy_number has been hit before it alerts you. While it is waiting for this timer to expire, it still will be scanning to make sure that the rsi_drop_limit is not hit. RSI is a slow moving metric, and you may want to set this to 10 minutes+ and even longer depending on the time horizon of your trades.

  
### Sell Orders  
--sell_order_type [basic_sell|ladder] : If your order is a sell order, you can pick what type of monitoring scan you would like to make. The two types are the basic_sell and the ladder. The basic sell will simply send you a sell signal message once a certain percentage of gain or loss is hit. For example, if you set the basic_sell_profit to '5', then you will receive your message when the price of the asset rises 5% above the price you bought it at. If you set your percent_loss_limit to '2', if the price of the asset drops 2% below the price you bought it at, DCD will send you the message that you need to sell due to the stop loss limit being reached.   
    - The 'ladder' option value is a bit complex but a useful value for this option. The ladder has quite a few dependent options, and each is outlined below in the 'Ladder Sell' section.

--asset_bought_price [Float or int] : The dollar price of the asset at the time you bought it, or if you don't know what that was, whatever the current price is, you want to compare the future price to calculate potential profits and losses. 

--percent_loss_limit [Float or int] : The percentage drop below the price you bought it for that you would allow the asset to drop in value before you would want to sell to minimize losses. You do not need to enter a negative sign '-' before the number; just enter a whole integer or decimal number like 5 for -5% and 3.14 for -3.14%.

--basic_sell_profit [Float or int] : The percentage gain you desire before DCD signals you to sell your position. If you want to gain 8% profit before you sell, just enter '8'.
##### Ladder Sell Dependent Options  
- For the ladder sell, you will need all the two above options as well as the ones below that will be prompted to you. The price you bought it for, the percentage of the stop-loss limit. The ladder sell scan will trigger when the percentage gain is wanted, and, rather than sell right away, start a timer to see if it gains more than the positive step gain percentage within that timer; otherwise, it sells. If the percentage increases above the step gain, reset the timer and wait again to see if it stagnates or keeps increasing in price. If the percentage is dropped below the original percent wanted at any time, sell immediately. If a higher percentage is found and you are up a 'rung', the negative step gain determines if you sell based on a percent loss relative to that new percentage gain. Example: Bought price is $100. The price goes to $105 and you set your minimum_ladder_profit to 5%, so the ladder sell scan initiates and waits the length of ladder timer value before deciding if it should sell or not. During that wait period, if the profit percentage drops below that 5% value at any time, it will trigger a sell signal. If the positive step gain is set to 1, if the asset price goes to $106, then a step of 1% profit has been climbed, and the timer resets. If the timer runs out and no more than a 5-6% gain is achieved, the sell order is initiated. If the asset jumps to $107, the ladder timer resets yet again to see if it will keep climbing within the timespan you set. If the negative step gain is set to 0.5, or half a percent, if the asset price drops to $106.5, it will alert you to sell before the timer expires. This is the basic premise of the ladder scan. Once the initial desired gain is wanted, rather than sell right away, wait it out and see if it keeps climbing, and if it drops a significant amount within the margins you set, then sell. 

 - This value may be modified in the future for less than second transactions and faster trades. The timer sensitivity value does the same thing but to the timer before it idles out and sells. Both sensitivity values are optional. If you want to basically hold on to the asset for as long until the negative value is what triggers the sell to hold onto as long as possible, just set the timer value to many hours.

--minimum_ladder_profit [Float or int]: The minimum amount of profit in a percentage you want to reach before the scan starts. Very similar to the basic_sell_profit except it doesn't execute the sell right away; it's just the minimum profit you want.

--ladder_step_gain [Float or int] : The step up in a percentage of profit you want before the ladder timer duration resets. If your minimum_ladder_profit is 5%, and this step gain is set to 1%, and the time is set to 1 hour, if you reach 5% profit, the timer will start for 1 hour, and then if you step up to 6%, the timer will restart and wait to sell because the price climbed one 'rung' higher in the ladder based on your 1% step.

--ladder_step_loss [Float or int] : The step down in percentage of profit you want to allow before the sell signal is initiated. By default, if you ever drop below the minimum_ladder_profit, it will trigger a sell signal no matter what to lock in that profit. If you set this to 0.5%, if the profits go to 6%, if they drop to 5.5%, the order will sell because it fell 0.5% below the highest profits reached. If the profit was 6%, then it goes to 6.25%; if it drops to 5.75%, it will also sell because a new high has been reached. 

--ladder_timer_duration [hours:minutes:seconds]: The timer value is set with hh:mm:ss format. If no time is used in a category, for example, setting the timer to 1 hour, then you still need zeros in the other slots, i.e., 00:01:00 is one hour. This is the amount of time you would like the ladder to wait to see if the profits will climb or drop before it lets you know to sell. If you want to basically hold on to the asset for as long until the negative value is what triggers the sell to hold onto as long as possible, just set the timer value to many hours.

  
--ladder_step_sensitivity [Float or int] : The step sensitivity value sets the number to divide the positive and negative step values by each time the timer is reset and a step in profit is gained. This makes the algorithm more sensitive to the profits dropping the higher you go. If you don't want to change the sensitivity of the algorithm with each step, just set this to 1. An example would be the first time you step up 1% for your ladder_step_gain; if you set this sensitivity value to 2, the next step gain is 0.5%, and the next time 0.5% is reached, then the next step gain is 0.25%, etc. This makes the algorithm more likely to lock in profits the higher the profits go.

--ladder_timer_sensitivity [Float or int] : The ladder sensitivity value also divides the timer duration by whatever number you set here. Similar to the ladder_step_sensitivity above, this makes the ladder more sensitive the higher the profits go. If you set this value to 2, if you set the timer for the ladder to an hour, then the second timer that activates when you make a step gain will be 30 minutes. If you want your time to be the same for every step up, just set this to 1.

  
### Profit Loss Algorithm Functions  
- The profit-loss algorithm informs you how much of the asset you should sell, or if you sell the whole amount, how much to keep of your new capital gained from the result of the trade. 

--profit_loss_finction [profit_harvest|swing_trade] : The profit loss function you only need to select if DCD is set to a sell type. The profit harvest function will calculate how much profit you made above your initial capital and how much you should keep of that profit. This strategy of profit harvesting is a safer strategy than full on swing trading because rather than selling your whole position and rebuying all at once, you can just sell the profits, and if you want to use the profits to buy back in, just buy back in the price has dropped with your initial capital in, and then once the price stabilizes back to your original price of the position, you're at a positive gain with less overall risk than selling the whole position. I will say that this mainly only works on assets that have more value and are less volatile, such as bitcoin, and something you don't mind actually keeping your capital in the asset itself and not just trying to maximize dollar profits, but rather gain more of the asset itself. If you can't remember how much profit or loss you made on previous trades, remember to use the ''--message_history view' option!   
    - The swing trade algorithm is intended to sell the entire position you are in, and then just use that new whole amount to buy your next position. This can theoretically maximize profits, but can also maximize losses. Only do this with good-quality assets, not degenerate shitcoins like Dogecoin. If you plan to do this, keep a tax treasury fund as if you swing trade massive amounts; even if you lose it all on a dip, you still owe tax on the short-term capital gains, or 15% of profit, i.e., if you trade from $10,000 up to $100k, $90,000 profit will likely be taxed at minimum 15%, or $13,500. If you end up losing it all because you majorly gamble, and drop back down to $10,000 only, capital loss is only a max of $3k per year, and you'd still owe $10.5k even if you don't have the money. Swing trading is risky with large amounts; be warned. I am not a financial advisor, and this is not financial advice. Just giving you a heads up so you don't screw over your life by being an ignorant donkey.

--swing_trade_skim [Float or int] : The percent of the profit percentage you would like to take if you are swing trading. This is like doing a hybrid of a profit harvest and swing trade, where you sell the whole position, but then keep some profits instead of buying all back in. This value is a percent of the profit, so if you gain 5% profits and want to keep half of the overall profits, you would enter 50 for this option value, NOT 2.5. If you do not want to take any profit to skim off, just enter 0 for this.
### Email Response Values and Commands  
- When you respond to the bot using email, compose a new message rather than replying to the email the bot sent you.  
- In the subject of the email, enter 'DCD' (the default). This can be changed to whatever you want in the config file.  
- Separate each value/command with a comma, such as 't:500,a:20'  
- Right now, there are only two values DCD needs, and it's only if you are logging a completed buy or sell order.  
-  The wait command tells the bot to sleep for a specified amount of time and then restart the scan. You may want to do this if you are unable to do the trade at that moment, missed the opportunity for the trade and want to have the bot re-scan, or based on your own perception of the market based on fundamental analysis instead of the purely technical this bot tracks, you might want to tell it to wait.  
- All three of these commands/values can be aliased to whatever you want in the config file, but must remain as separated with the key name and the value as a colon and each separate key value pair separated by a comma.

t:total_dollar_amount : This is the total dollar amount as an integer or float that you bought or sold in the order AFTER FEES. Whatever final amount you have after a sell or the dollar amount you used for your buy, that is the dollar total amount.

a:total_asset_amount : This is the total asset amount you bought or sold as an integer or float. If you bought 0.1 Bitcoin, then 0.1 is the total_asset_amount

w:hh:mm:ss :  The wait command tells the bot to sleep for the time you specify with the hours:minutes:seconds syntax. 

  
### Some Final Words  
- You don't have to do full-on daytrading. You can simply use this to more efficiently dollar cost average into bitcoin or make larger, less risky swing trades a few times a month for a little extra fun money. 

- Before using this program for daytrading, you should know some basics of how the crypto markets work, daytrading theory, have no attachment to your trading money, understand what cryptos are trash and which ones will always have some good value so you don't get asbolutely wrecked if you don't use your stop loss and get stuck in a position right into a bear market. Daytrading is dangerous; you can lose a lot of money, and it's even more dangerous daytrading in the even more volatile crypto market. I called this program 'Degenerate Crypto Daytrader' because full-time daytraders are degenerates. It's a waste of time constantly checking prices and analyzing charts instead of just learning a useful skill and getting compensated for your labor and actually contributing to the world. However, if you don't have to spend your time monitoring and you actually trade good cryptos, which helps create liquidity for the asset, then why not? That's what this program solves for me and could solve for you.

- Bitcoin, Monero, Cardano's ADA, and Hedera's HBAR are the only four crypto projects that are worth a damn and have any real world long-term value and utility (I spent months researching every, yes, every, layer 1 crypto to come to this conclusion, so no, I'm not pulling it out of my ass or am part of a stupid cult for any of these coins). What this means is that even if they drop really badly in a day, they have enough value that it's extremely unlikely they will absolutely tank if you get in a bad position. THIS IS NOT FINANCIAL ADVICE, just my personal opinion. Once again, if you listen to your stop loss, which this program will notify you of, then that shouldn't be happening, but if you hodl yourself into a hole, sticking with these three, you should be far less likely to get crushed in double-digit % losses.

### Support  
- If you have any questions about using the programs or how it works or even want to modify and contribute, feel free to open an issue on this projects GitHub page or send me an email at EnlightenedMeathead at protonmail dot com. If you know me irl, just come up and ask or dm me on whatever platform you know me.

### License
- This project is licensed under the GNU General Public License v2.0 (GPLv2). See the LICENSE file for details.

# **Legal Notice**

- The trades executed using this program are performed solely by the user. Any recommendations or information provided in this documentation are not financial advice and should not be interpreted as such. The author of this program is not a licensed financial advisor. The use of this program is at the user’s own risk. This program employs algorithms to perform mathematical calculations of potential profits or losses based on user input, but the output may not be fully accurate. By using this program, you agree that you are solely responsible for any losses incurred from trades, and the author accepts no legal or financial responsibility for any such losses.
