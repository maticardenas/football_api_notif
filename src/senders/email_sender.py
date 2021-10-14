import smtplib

from config.email_notif import SMTP_SERVER, GMAIL_SENDER, GMAIL_PASSWD

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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


def send_email_html(subject: str, body: str, recipient: str) -> None:
    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.ehlo()
    server.starttls()
    server.login(GMAIL_SENDER, GMAIL_PASSWD)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = recipient

    html = f"""\
    <html>
      <head></head>
      <body>
        {body}
      </body>
    </html>
    """

    part1 = MIMEText(body, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        server.sendmail(GMAIL_SENDER, [recipient], msg.as_string())
        print('email sent')
    except Exception as e:
        print(f'error sending mail {e}')

    server.quit()





