# Module for notifying the user when a or buy or sell scan has triggered a signal.
import smtplib
import imaplib
import email
import time

import gnupg
from email.mime.text import MIMEText
from email.header import decode_header
from resources import creds


# Send yourself a PGP encrypted email using a Gmail for the sender and whichever PGP compatible email recipient you want
def notify_email(subject, message, public_key=None):
    # If no key was passed, try finding one in the creds file
    try:
        public_key = creds.public_key
    except Exception as e:
        # If the encryption key is not found, still send the email unencrypted
        print(f"Error getting public key from creds file: {e}. If you didn't want to encrypt the email, ignore this "
              f"message. If you do want to encrypt, YOU MAY NEED TO SET THE TRUST OF THE PUBLIC GPG KEY YOU PUT IN "
              f"YOUR CONFIG/CREDS FILE TO ULTIMATE FOR THIS TO WORK. This can be done by going to the directory the "
              f"creds file is stored that has your public key string as a variable and open a python3 console, then "
              f"typing these commands:"
              f"\n>>> import gnupg"
              f"\n>>> gpg = gnupg.GPG()"
              f"\n>>> import creds"
              f"\n>>> pub = creds.public_key"
              f"\n>>> pub = gpg.import_keys(pub)"
              f"\n>>> fin = pub.fingerprints[0]"
              f"\n>>> gpg.trust_keys(fin, 'TRUST_ULTIMATE') ")

    # Create and encrypt the email message if gpg key is provided
    if public_key is not None:
        gpg = gnupg.GPG()
        public_key = gpg.import_keys(public_key)
        recipient_fingerprint = public_key.fingerprints[0]
        final_message = gpg.encrypt(str(message), recipient_fingerprint)
    else:
        final_message = message
    # Create the email message`
    msg = MIMEText(str(final_message))
    msg["Subject"] = subject
    msg["From"] = creds.sender_email
    msg["To"] = creds.recipient_email

    # SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = creds.sender_email
    smtp_password = creds.sender_password

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS encryption
        server.starttls()
        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(creds.sender_email, creds.recipient_email, msg.as_string())
    print("Email notification sent successfully.")

# Recursively check the email if it is multipart for plain text section that is the body
def get_plain_text_body(message):
    # If the message is multipart, iterate over the parts
    if message.is_multipart():
        for part in message.get_payload():
            content_type = part.get_content_type()
            print(f"Part content type: {content_type}")  # Log content type of each part
            # Recursively check each part for plain text
            result = get_plain_text_body(part)
            if result:
                return result
    else:
        # If the message is not multipart, check if it is plain text
        content_type = message.get_content_type()
        print(f"Message content type: {content_type}")  # Log content type of the message
        if content_type == "text/plain":
            # Decode the body from bytes and return the text value
            return message.get_payload(decode=True).decode()
    return None


def check_email_response(timeout=creds.email_check_timeout, check_interval=creds.email_check_interval):
    print("Starting email reply checker...")
    email_to_check = creds.sender_email
    password = creds.sender_password
    search_subject = creds.email_subject_check
    end_time = time.time() + timeout
    #try:
    while time.time() < end_time:
        # Open an ssl connection
        with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(email_to_check, password)
            mail.select('inbox')
            # Check for unseen emails and return the status if the command was successful
            status, messages = mail.search(None, 'UNSEEN')
            # Iterate through all unseen messages
            for message_ID in messages[0].split():
                print(f"searching message: {message_ID}")
                status, msg_data = mail.fetch(message_ID, '(RFC822)')
                for response_part in msg_data:
                    # Make sure you get the tuple of the header and the content for that header
                    if isinstance(response_part, tuple):
                        # Get the content from that header and check if the header is the Subject
                        message = email.message_from_bytes(response_part[1])
                        subject = decode_header(message['Subject'])[0][0]
                        # If the header isn't already decoded (Some email systems won't decode in
                        # message_from_bytes)
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                        # If the search subject the user assigns in the config is equal to the subject of the email
                        if search_subject in subject:
                            body = get_plain_text_body(message)
                            if body:
                                print(f"Received email back containing: {body}")
                                return body
                            else:
                                print("No plain text body found in the email.")
                                return None
        time.sleep(check_interval)
    print("Email response check timed out!")
    #except Exception as e:
    #    print(f"Email function for waiting for response error: {e}")


def email_reply_parser(email_response):
    # Get the response, see if told to wait, or try and parse the total amount of capital received for the trade
    # and the asset amount sold
    try:
        email_str = str(email_response)
        email_values = email_str.split(',')
        email_values_dict = {}
        email_response_dict = {}
        for value in email_values:
            key, value = value.split(':')
            email_values_dict[key.strip()] = value.strip()
        for key, value in creds.email_response_keys.items():
            if key in email_values_dict.keys():
                variable_key_name = creds.email_response_keys[key]
                email_response_dict[variable_key_name] = email_values_dict[key]
        print(email_response_dict)
        return email_response_dict
    except Exception as e:
        print(f"Unable to convert email response to key value pairs: {e}")


def email_value_assigner(email_response_dict):
    global asset_amount_sold, asset_sold_total
    try:
        if 'asset_sold_total' in email_response_dict.keys():
            asset_sold_total = float(email_response_dict['asset_sold_total'])
            print(f'asset sold for: {asset_sold_total}')
        if 'asset_amount_sold' in email_response_dict.keys():
            asset_amount_sold = float(email_response_dict['asset_amount_sold'])
            print(f'asset amount sold: {asset_amount_sold}')
        return asset_amount_sold, asset_sold_total
    except Exception as e:
        print(f'Unable to convert email values to variables needed for logging function in email_value_assigner: {e}')


if __name__ == "__main__":
    #notify_email('dcdt', f"test not encrypt new")
    #check_email_response(20, 10)
    email_response = email_reply_parser('a:100.27,t:82')
    email_value_assigner(email_response)
    pass
