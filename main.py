""" main.py """

import os
from dotenv import load_dotenv
from whatsapp import WhatsAppAPI

load_dotenv()


def main():
    """ main """

    access_token = os.getenv("ACCESS_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")
    recipient_phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")

    if not all([access_token, phone_number_id, recipient_phone_number]):
        print("Erişim bilgileri eksik! .env dosyasındaki tüm bilgileri kontrol edin.")
        return

    whatsapp_api = WhatsAppAPI(access_token, phone_number_id)

    message = "Merhaba! WhatsApp Cloud API ile mesaj gönderildi."
    response = whatsapp_api.send_text_message(recipient_phone_number, message)
    print(response)

    media_url = "https://example.com/your-image.jpg"
    caption = "Bu bir örnek resim."
    response = whatsapp_api.send_media_message(recipient_phone_number, media_url, caption)
    print(response)


if __name__ == "__main__":
    main()
