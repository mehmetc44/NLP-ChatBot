import requests
import random
class RasaClient:

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
        return test[random.randint(1,5)]