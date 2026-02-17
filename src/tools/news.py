import os
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv()


class News:
    def __init__(self):
        self._url = f"https://gnews.io/api/v4/top-headlines?country=br&category=nation&apikey={os.getenv("GNEWS_API_KEY")}"

    def read_news(self):
        user_message = "Me ataulize sobre as ultimas noticias:\n"

        response = requests.get(self._url)

        if response.status_code >= 400:
            user_message = "Nada foi encontrado..."

        if response.status_code == 200:
            articles: list[dict[str, Any]] = response.json()["articles"]
            for article in articles:
                user_message += f"{article["title"].title()}:\n"
                user_message += f"{article["content"]}\n"
                user_message += f"Fonte: {article["url"]}\n"
                user_message += f"Data de publicação: {article["publishedAt"]}\n"

            user_message += "Seja bem informativa e organizada com as no0ticias."
        return user_message
