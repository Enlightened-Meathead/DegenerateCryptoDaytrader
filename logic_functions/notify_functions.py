# Module for notifying the user when a or buy or sell scan has triggered a signal.
import smtplib
import gnupg
from email.mime.text import MIMEText


# Send yourself a PGP encrypted email using a Gmail for the sender and whichever PGP compatible email recipient you want
def not_notify_email(subject, message):
    # Get the emails and public key from the creds file
    import resources.creds as creds

    # Create and encrypt the email message
    gpg = gnupg.GPG()
    public_key = gpg.import_keys(creds.public_key)
    recipient_fingerprint = public_key.fingerprints[0]
    encrypted_message = gpg.encrypt(str(message), recipient_fingerprint)
    # Create the email message`
    msg = MIMEText(str(encrypted_message))
    msg["Subject"] = subject
    msg["From"] = creds.sender_email
    msg["To"] = creds.recipient_email

    # SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = creds.smtp_username
    smtp_password = creds.smtp_password

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS encryption
        server.starttls()
        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(creds.sender_email, creds.recipient_email, msg.as_string())
    print("Email notification sent successfully.")


if __name__ == "__main__":
    profit = 10
    #notify_email('dcdt', f"test {profit}")
    pass
import smtplib
from email.mime.text import MIMEText
import gnupg
import resources.creds as creds


def notify_email(subject, message):
    # Print subject and message to verify input
    print(f"notify_email - Subject: {subject}")
    print(f"notify_email - Message: {message}")

    # Create and encrypt the email message
    gpg = gnupg.GPG()
    public_key = gpg.import_keys(creds.public_key)
    recipient_fingerprint = public_key.fingerprints[0]

    encrypted_message = gpg.encrypt(message, recipient_fingerprint)
    print(f"Type of encrypted_message: {type(encrypted_message)}")
    print(f"Encryption Status: {encrypted_message.status}")
    print(f"Encryption OK: {encrypted_message.ok}")
    print(f"Encryption Stderr: {encrypted_message.stderr}")

    if not encrypted_message.ok:
        raise Exception('Encryption failed: ' + str(encrypted_message.status) + ' ' + str(encrypted_message.stderr))

    # Convert encrypted message to string
    encrypted_message_str = str(encrypted_message)
    print(f"Encrypted Message: {encrypted_message_str}")

    # Check if the encrypted message is empty
    if not encrypted_message_str.strip():
        raise Exception('Encrypted message is empty')

    # Create the email message
    msg = MIMEText(encrypted_message_str)
    msg["Subject"] = subject
    msg["From"] = creds.sender_email
    msg["To"] = creds.recipient_email

    # Print the email details before sending
    print(f"Email - Subject: {msg['Subject']}")
    print(f"Email - From: {msg['From']}")
    print(f"Email - To: {msg['To']}")
    print(f"Email - Body: {msg.get_payload()}")

    # SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = creds.smtp_username
    smtp_password = creds.smtp_password

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS encryption
        server.starttls()
        # Log in to the SMTP server
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(creds.sender_email, creds.recipient_email, msg.as_string())
    print("Email notification sent successfully.")


# Test the function
if __name__ == '__main__':
    try:
        # main()
        sub = 'test subject'
        mes = "yet another test!"
        notify_email(sub, mes)
    finally:
        print("Bot finished!")