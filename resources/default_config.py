## Degenerate Crypto Daytrader Config File. If this is the default config, DO NOT ALTER THIS FILE, make a copy and
# name it config.py

# For now, this config file will just be self contained in the programs directory until I decide if i will be making
# it a package that can be installed, at which point i will place the config file in the users config directory

# If you do not set email configurations, you can still use this program just as the bot_type of desktop_notify

# The timeout for the desktop notification function before it disappears. If you want your desktop notification to
# stay up so you for sure see it, set this to 'None'
#desktop_notification_timeout = None
desktop_notification_timeout = 3000

# Whether you will also get a desktop notification when the notify message is sent if you are using an email
# to notify you. If you just want the email notification and no desktop notification, set this to False
#desktop_notify_with_email = False
desktop_notify_with_email = True

# The email account you would like to remotely authenticate to and send the notifications from. YOU MUST make a
# separate, standalone email for this program that has no confidential or personal data. This program was designed
# for use with gmail as the sender, so I highly recommend you just create a gmail account to use for sending the
# notifications. If you don't care about using GPG to send to something like proton mail, then you can also use this
# email as the recipient email and just email itself for your notifications and remote commands
sender_email = "@gmail.com"

# The app password for the email account. This password is just for use with remote app authentication, and cannot be
# used for regular sign ins.  In gmail, you can get a remote app password at this link:
# https://support.google.com/accounts/answer/185833?hl=en/ . You need 2FA enabled to create app passwords. Because of
# the simple nature of this program, this why I say you MUST create a separate email for this program and not use
# that email for anything else as this credential is exposed in this file. Granted, your computer should have a
# strong password at logon, and hopefully a boot password too, so in order to compromise your throwaway email they
# have to find this app password in the config file, then create a python script or modify this programs to pull down
# your email inbox. Which, if you followed the instructions and made a dedicated throwaway gmail, they just hacked
# into a big nothing burger. In order to log in to the web client, a would be hacker would need your original account
# password and your 2FA device, so even if this is found, once again, should be a nothing burger. Plus, if you have
# someone who broke into your account and is reading your config files for passwords, I think you have bigger
# problems on your hands ;) In the future I may make this more secure to make it more convenient to just use an
# existing email, but for now making a throwaway gmail is easy and the worse that can happen is someone finds your
# responses, which they probably wouldn't even understand ¯\_(ツ)_/¯
sender_password = "16 digit app password"

# The email account that receives the full sentence notifications from the bot that contains the somewhat sensitive
# data of how much to buy/sell, profit losses, etc. If you care about privacy, I recommend using proton mail and then
# exporting your public key and putting it in this file above. If you don't care if your email provider reads this
# data, then you can use your throwaway email or send the notifications to whatever email you want. The email
# notifications automatically detect if you want to use GPG encryption, so if you don't have GPG key, the email will
# send
recipient_email = "@protonmail.com"

# The GPG public key of the recipient email you would like to encrypt your emails with before you send them over
# whatever email servers you are going to be user. This is OPTIONAL, and if you leave this blank, your emails will
# still send over regular TLS based email services, just not locally encrypted before the message is sent.
public_key = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Your pgp key
-----END PGP PUBLIC KEY BLOCK-----"""

# The subject of the email you want the bot to recognize as an incoming command. Basically, when you send an email
# back to the bot's sender_email, write whatever exact string you set here that you want it to respond to
email_subject_check = "DCD"

# The length in seconds after a scan find a buy or sell signal the bot will wait for an email response. If the signal
# is still true, you will get another email right after, so by default if you miss the first notification,
# if the signal is still true it will be pushing you notification every 10 minutes.
email_check_timeout = 600

# How often to check the email inbox after you are authenticated and scanning for email responses. Gmail has an API
# guide on their limits, but every 10 seconds is far above the limit and fast enough for a simple notification bot.
email_check_interval = 10

# The keys in this dictionary are what you are going to assign the commands value to in your email response following
# the key:value,key:value syntax. For example, if you followed the buy signal and bought 0.5 of the asset for
# $100.00, you would email back t:100,a:0.5 and the email scanner would parse these values to be logged in the
# spreadsheet if it is done. If you want to change the key values, change those in the dictionary below like
# 'total':'email_dollar_total'
user_response_keys = {'t': 'response_dollar_total', 'a': 'response_asset_amount', 'w': 'bot_time_to_wait'}

# In your DCD history file, the alias of the command you want it to write to for the one lines, so you can copy and
# paste previous trades easier if you change the program alias in you shell.
repeat_one_liner_alias = "degenerate_crypto_daytrader"

# This is the filepath the bot will use to write your excel data to your workbook. If you enter a path, create the
# workbook with this program using the --create_workbook option. If you are not logging your trades, you don't need
# to enter this.
trade_log_path = "/home/username/"
