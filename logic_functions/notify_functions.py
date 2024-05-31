# Module for notifying the user when a or buy or sell scan has triggered a signal.
import smtplib
import gnupg
from email.mime.text import MIMEText

import resources.creds as creds


# To do: enable pgp encryption, have a way the subject and message passed to the email function that gives information
def notify_email(subject, message):
    # Email details
    sender_email = creds.sender_email
    recipient_email = creds.recipient_email

    # Create and encrypt the email message
    gpg = gnupg.GPG()
    public_key = gpg.import_keys(creds.public_key)
    recipient_fingerprint = public_key.fingerprints[0]
    encrypted_message = gpg.encrypt(message, recipient_fingerprint)

    # Create the email message`
    msg = MIMEText(str(encrypted_message))
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = creds.smtp_username
    smtp_password = creds.smtp_password

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS encryption
        server.starttls()
        # Log in to the SMTP server (if authentication is required)
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully.")