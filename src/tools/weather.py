import os
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv()


class Weather:
    def __init__(self, city: str = "LA"):
        self._city: str = city
        self._url = f"http://api.weatherapi.com/v1/current.json?max=10&key={os.getenv("WEATHER_API_KEY")}&lang=pt&q={self._city}"

    def get_weather(self) -> str:
        user_message: str = (
            "Preciso que de acordo com os dados climáticos, você faça:\n"
        )
        user_message += "- Analise de segurança\n"
        user_message += "- Dar dicas de saúde\n"
        user_message += "Organize os seguintes dados:\n"

        response = requests.get(self._url)

        if response.status_code >= 400:
            user_message = "Não foi possível fornecer o clima..."

        if response.status_code == 200:
            data = response.json()
            location: dict[str, Any] = data["location"]
            name = location["name"]
            region = location["region"]
            country = location["country"]
            lat = location["lat"]
            lon = location["lon"]
            time = location["localtime"]
            # location
            user_message += f"- Localização: {name}\n"
            user_message += f"- Região: {region}\n"
            user_message += f"- País: {country}\n"
            user_message += f"- Latitude: {lat}\n"
            user_message += f"- Longitude: {lon}\n"
            user_message += f"- Horário Local: {time}\n"
            # weather
            weather: dict[str, Any] = data["current"]
            last_update = weather["last_updated"]
            temp_c = weather["temp_c"]
            temp_f = weather["temp_f"]
            feels_c = weather["feelslike_c"]
            feels_f = weather["feelslike_f"]
            humidity = weather["humidity"]
            condition = weather["condition"]["text"]
            pressure = weather["pressure_mb"]
            wind_speed = weather["wind_kph"]

            user_message += f"- Ultima atualização: {last_update}\n"
            user_message += f"- Temperatura em ˚C (Celsius): {temp_c}\n"
            user_message += f"- Temperatura em ˚F (Fahrenheit): {temp_f}\n"
            user_message += f"- Sensações térmicas (Celsius, Fahrenheit):\n"
            user_message += f"  - ˚C: {feels_c}\n"
            user_message += f"  - ˚F: {feels_f}\n"
            user_message += f"- Humidade: {humidity}\n"
            user_message += f"- Condição: {condition}\n"
            user_message += f"- Pressão: {pressure}\n"
            user_message += f"- Velocidade dos ventos (Km/h): {wind_speed}\n"

        user_message += "Explique ao usuário de forma clara, em português."
        return user_message
