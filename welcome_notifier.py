#!/bin/env python
from config.whatsapp_notif import RECIPIENTS
from src.emojis import Emojis
from src.senders.whatsapp_sender import send_whatsapp_message

if __name__ == "__main__":
    for recipient in RECIPIENTS:
        message = f"{Emojis.WAVING_HAND.value}Hola {recipient}\n\n" \
                  f"Finalmente la aplicación fué deployada en AWS y está lista para notificarte con la información" \
                  f" mas detallada y personalizada que puedas encontrar acerca de Futbol y Messi." \
                  f"\n\n P.D.: Crapema arrugó y todavía no se registró"
        send_whatsapp_message(RECIPIENTS[recipient], message)