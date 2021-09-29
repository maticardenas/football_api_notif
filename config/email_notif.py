import smtplib

RECIPIENTS = [
    # CONFIGURE HERE YOUR RECIPIENTS SEPARATED BY COMMA
]

# GMAIL

SMTP_SERVER = smtplib.SMTP('smtp.gmail.com', 587)

GMAIL_SENDER = 'sender_email@gmail.com'
GMAIL_PASSWD = 'sender_password'