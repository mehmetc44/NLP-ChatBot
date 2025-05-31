import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class ActionFindWeather(Action):
    def name(self) -> Text:
        return "action_find_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        date = tracker.get_slot("date")

        if not city:
            dispatcher.utter_message(text="Please specify a city name.")
            return []

        try:
            api_key = "6dbb9089834a6108c1f48b565f95bdb2"
            units = "metric"
            lang = "en"

            forecast_url = (
                f"http://api.openweathermap.org/data/2.5/forecast?"
                f"q={city}&appid={api_key}&units={units}&lang={lang}"
            )
            forecast_data = requests.get(forecast_url).json()


            target_date = date
            daily_forecasts = [
                forecast for forecast in forecast_data['list']
                if forecast['dt_txt'].startswith(target_date)
            ]

            if not daily_forecasts:
                dispatcher.utter_message(text=f"No forecast data found for {target_date} in {city.title()}.")
                return []

            message_parts = [
                f"Weather forecast for {city.title()} on {target_date}:"
            ]
            for forecast in daily_forecasts:
                time = forecast['dt_txt'][11:16]
                desc = forecast['weather'][0]['description']
                temp = forecast['main']['temp']
                message_parts.append(f"{time}: {desc}, {temp}°C")

            dispatcher.utter_message(text="\n".join(message_parts))

        except requests.exceptions.RequestException:
            dispatcher.utter_message(
                text="Sorry, I couldn't connect to the weather service. Please try again later."
            )
        except KeyError:
            dispatcher.utter_message(
                text="Sorry, I couldn't find weather data for that location."
            )
        except Exception as e:
            dispatcher.utter_message(
                text="An unexpected error occurred. Please try again."
            )

        return []