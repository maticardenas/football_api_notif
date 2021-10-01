#!/bin/env python
from config.whatsapp_notif import RECIPIENTS
from src.emojis import Emojis
from src.senders.whatsapp_sender import send_whatsapp_message

if __name__ == "__main__":
    for recipient in RECIPIENTS:
        message = f"{Emojis.WAVING_HAND.value}Hola {recipient}\n\n" \
                  f"Finalmente la aplicación fué deployada en AWS y está lista para notificarte con la información" \
                  f" futbolistica y personalizada que desees. No te olvides de sugerir cualquier cambio o mejora" \
                  f"\n\n P.D.: Crapema arrugó y todavía no se registró"
        send_whatsapp_message(RECIPIENTS[recipient], message)