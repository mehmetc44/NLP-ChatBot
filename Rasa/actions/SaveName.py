from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3


class ActionSaveNameToSQL(Action):

    def name(self) -> Text:
        return "action_save_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        user_name = tracker.get_slot("name")

        if user_name:

            conn = sqlite3.connect("data/users.db")
            cursor = conn.cursor()


            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)


            cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
            conn.commit()
            conn.close()

            dispatcher.utter_message(text=f"Thanks {user_name}, Your entry has been saved to the database")
        else:
            dispatcher.utter_message(text="I could not catch your name! Can you repeat your name please?")

        return []
