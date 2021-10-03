import smtplib

from config.email_notif import SMTP_SERVER, GMAIL_SENDER, GMAIL_PASSWD

def send_email(subject: str, body: str, recipient: str) -> None:
    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.ehlo()
    server.starttls()
    server.login(GMAIL_SENDER, GMAIL_PASSWD)
    body = f"Subject: {subject} \n\n{body}"

    try:
        server.sendmail(GMAIL_SENDER, [recipient], body.encode('ascii', 'ignore').decode('ascii'))
        print('email sent')
    except Exception as e:
        print('error sending mail')

    server.quit()



