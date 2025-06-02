import sqlite3
from rasa_sdk import Action


class ActionFindContinent(Action):
    def name(self):
        return "action_find_continent"

    def run(self, dispatcher, tracker, domain):
        country = tracker.get_slot("country")

        conn = sqlite3.connect("data/ContinentOfCountries.db")
        cursor = conn.cursor()

        country = country.strip().capitalize()

        cursor.execute("SELECT continent FROM country_continent WHERE LOWER(country) = LOWER(?)", (country,))
        result = cursor.fetchone()

        conn.close()

        if result:
            dispatcher.utter_message(text=f"The country of {country} : {result[0]}")
        else:
            dispatcher.utter_message(text=f"I could not find a continent information for {country} ")

        return []