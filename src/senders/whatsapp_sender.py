from twilio.rest import Client

from config.whatsapp_notif import TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN, TWILIO_WHATSAPP_NUMBER, RECIPIENTS

client = Client(
    username=TWILIO_ACCOUNT_SID,
    password=TWILIO_ACCOUNT_TOKEN
)

def send_whatsapp_message(recipient: str, text: str) -> None:
    client.messages.create(body=text,
                           from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
                           to=f"whatsapp:{recipient}")