"""import openai"""
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionOpenAIResponse(Action):
    def name(self):
        return "action_openai_response"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        openai.api_key = "YOUR_OPENAI_API_KEY"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )

            reply = response['choices'][0]['message']['content']
            dispatcher.utter_message(text=reply)

        except Exception as e:
            dispatcher.utter_message(text=f"Error calling OpenAI API: {str(e)}")

        return []
