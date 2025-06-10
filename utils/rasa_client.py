import requests
import random
class RasaClient:
    def send_message_to_rasa(self, user_id: str, message: str) -> list[str]:
        url = "rasaURL"
        payload = {
            "sender": user_id,
            "message": message
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                responses = response.json()
                return [item['text'] for item in responses if 'text' in item]
            else:
                return [f"Error: Rasa did not respond (status code: {response.status_code})"]
        except Exception as e:
            return [f"Connection error: {str(e)}"]

    def send_test_message(self):
        test = [
        "Teşekkür ederim, iyiyim! Sen nasılsın?",
        "Harikayım, seninle sohbet etmek güzel!",
        "Gayet iyiyim, senin günün nasıl geçiyor?",
        "İyiyim, sağ ol! Sen nasılsın?",
        "Enerjim yerinde, umarım sen de iyisindir!",
        "İyiyim, sohbetimize başladığıma sevindim!",
        "Şu an gayet mutluyum, sen nasılsın?",
        "Teşekkürler, iyiyim! Seninle konuşmak hep iyi geliyor.",
        "Harika hissediyorum, senin keyfin yerinde mi?",
        "İyiyim, senin için nasıl yardımcı olabilirim?"
        ]
        return test[random.randint(1,11)]