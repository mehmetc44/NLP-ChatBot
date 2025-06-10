from rasa_sdk import Action


class ActionWelcome(Action):
    def name(self):
        return "action_welcome"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Hello, I am Natasha. How can I help you?")
        return []