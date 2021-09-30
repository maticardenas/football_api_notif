from config.email_notif import SMTP_SERVER, GMAIL_SENDER, GMAIL_PASSWD, RECIPIENTS

def send_email(subject: str, body: str) -> None:
    server = SMTP_SERVER
    server.ehlo()
    server.starttls()
    server.login(GMAIL_SENDER, GMAIL_PASSWD)
    body = f"Subject: {subject}: \n\n{body}"

    try:
        server.sendmail(GMAIL_SENDER, RECIPIENTS, body.encode('ascii', 'ignore').decode('ascii'))
        print('email sent')
    except Exception as e:
        print('error sending mail')

    server.quit()



