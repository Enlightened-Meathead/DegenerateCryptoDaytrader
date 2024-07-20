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


def check_email_response(timeout=creds.email_check_timeout, check_interval=creds.email_check_interval):
    email_to_check = creds.sender_email
    password = creds.sender_password
    search_subject = creds.email_subject_check
    end_time = time.time() + timeout
    try:
        while time.time() < end_time:
            with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
                mail.login(email_to_check, password)
                mail.select('inbox')
                # Check for unseen emails and return the status if the command was successful
                status, messages = mail.search(None, 'UNSEEN')
                for message_ID in messages[0].split():
                    print(f"searching message: {message_ID}")
                    status, msg_data = mail.fetch(message_ID, '(RFC822)')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            message = email.message_from_bytes(response_part[1])
                            print(message)
                            subject = decode_header(message['Subject'])[0][0]
                            print(subject)
                            if isinstance(subject, bytes):
                                subject = subject.decode()
                            if search_subject in subject:
                                if message.is_multipart():
                                    for part in message.get_payload():
                                        if part.get_content_type() == "text/plain":
                                            body = part.get_payload(decode=True).decode()
                                else:
                                    body = message.get_payload(decode=True).decode()
                                print(f"Recieved email back containing: {body}")
                                return body
            time.sleep(check_interval)
    except Exception as e:
        print(f"Email function for waiting for response error: {e}")


if __name__ == "__main__":
    #notify_email('dcdt', f"test not encrypt new")
    check_email_response(20, 10)
    pass
