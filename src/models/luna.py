import json
import os
from typing import Any
import ollama
from dotenv import load_dotenv

from src.models.itt import ITT
from src.models.memory import Memory
from rich import console, markdown, live

from src.tools.dollar_search import DollarSearch
from src.tools.news import News
from src.tools.weather import Weather

load_dotenv()


class Luna:
    def __init__(
        self,
        model: str = "gemma2:2b",
        online: bool = False,
        memory: Memory = Memory(),
    ):
        self.__model: str = model
        self.__online: bool = online
        self.__host: str = (
            "127.0.0.1:11434" if not self.__online else os.getenv("OLLAMA_HOST_IP")
        )
        self.__client: ollama.Client = ollama.Client(self.__host)
        self.__memory: Memory = memory
        self.__options: dict[str, Any] = {
            "num_ctx": 4096,
            "temperature": 0.5,  # Equilíbrio: nem robótico (0.1), nem caótico (0.9).
            "top_p": 0.8,  # Permite um vocabulário variado sem perder o foco.
            "top_k": 30,  # Limita a escolha às 30 palavras mais prováveis.
            "repeat_penalty": 1.18,  # Valor padrão do Ollama para fluidez natural.
            "num_thread": 4,
        }
        self.__console: console.Console = console.Console()
        self.__md: markdown.Markdown = None

    def _load_simple_commands(self) -> dict[str, Any]:
        money_api = DollarSearch()
        news_api = News()
        COMMANDS = {
            "dolar hoje": money_api.search,
            "ler jornal": news_api.read_news,
        }

        return COMMANDS

    def _render_message(self, user_message: str):
        self.__memory.add_user_message(user_message)

        chat = self.__client.chat(
            model=self.__model,
            messages=self.__memory.get_memory(),
            stream=True,
            options=self.__options,
        )

        with live.Live(console=self.__console, refresh_per_second=10) as response:
            markdown_content = ""
            for chunk in chat:
                token = chunk["message"]["content"]
                markdown_content += token

                self.__md = markdown.Markdown(markdown_content)
                response.update(self.__md)

        self.__memory.add_assistent_response(markdown_content)

    def get_response(self, user_message: str) -> None:
        for command, callback in self._load_simple_commands().items():
            if command in user_message.lower():
                response = callback()
                self._render_message(response)
                break

        if user_message != "" and user_message not in self._load_simple_commands():
            self._render_message(user_message)
