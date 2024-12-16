""" whatsapp.py """

import requests


class WhatsAppAPI:
    """ Whatsapp API"""

    def __init__(self, access_token, phone_number_id):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"

    def send_text_message(self, recipient_phone_number, message):
        """ Send Text Message"""

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Mesaj Gönderim Verisi
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "text": {"body": message}
        }

        # POST isteği gönderme
        response = requests.post(self.url, headers=headers, json=data)

        # Yanıtı kontrol et
        if response.status_code == 200:
            print("Mesaj başarıyla gönderildi!")
            return response.json()  # JSON yanıtını döndürüyor
        else:
            print(f"Mesaj gönderilemedi. Hata kodu: {response.status_code}")
            return response.text  # Hata mesajı

    def send_media_message(self, recipient_phone_number, media_url, caption=""):
        """
        Resim, video gibi medya mesajları göndermek için kullanılır.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Medya mesajı için veri
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "image": {
                "link": media_url,
                "caption": caption
            }
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            print("Medya mesajı başarıyla gönderildi!")
            return response.json()
        else:
            print(f"Medya mesajı gönderilemedi. Hata kodu: {response.status_code}")
            return response.text
