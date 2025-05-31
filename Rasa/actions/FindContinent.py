import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet




class ActionFindContinentAPI(Action):
    def name(self) -> Text:
        return "action_find_continent_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        country = tracker.get_slot("country")

        if not country:
            dispatcher.utter_message(text="I did not get What country you meant")
            return []


        try:
            url = f"https://restcountries.com/v3.1/name/{country}"
            response = requests.get(url)

            if response.status_code != 200:
                dispatcher.utter_message(text="I could not find the country. please try again")
                return []

            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                region = data[0].get("region", "Bilinmiyor")
                subregion = data[0].get("subregion", "Bilinmiyor")
                dispatcher.utter_message(
                    text=f"{country.capitalize()} is in the continent of {region} , it is in the part of {subregion} ."
                )
                return [SlotSet("continent", region)]
            else:
                dispatcher.utter_message(text="Cevap boş döndü. Ülke adı geçerli mi?")
                return []

        except Exception as e:
            dispatcher.utter_message(text=f"API çağrısı sırasında hata oluştu: {e}")
            return []