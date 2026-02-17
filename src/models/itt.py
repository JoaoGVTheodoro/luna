import json
import os
import ollama
from dotenv import load_dotenv

load_dotenv()


class ITT:
    def __init__(self, path: str = os.getenv("CLUSTER_PATH"), online: bool = False):
        self._PATH: str = path
        self.__online: bool = online
        self.__host: str = (
            "127.0.0.1:11434" if not self.__online else os.getenv("OLLAMA_HOST_IP")
        )
        self.__client: ollama.Client = ollama.Client(self.__host)
        self._prompt_content: str = self._load_prompt()
        self._documents: list[str] = [
            os.path.join(self._PATH, document) for document in os.listdir(self._PATH)
        ]

    def _load_prompt(self) -> str:
        prompt = ""
        with open(os.getenv("CUSTOM_VISION_PROMPT"), "r", encoding="utf-8") as file:
            data = json.load(file)
            prompt += f"{data['objective']} e {data['rules']}"
        return prompt if prompt != "" else "Oque você está vendo?"

    def _get_last_doc(self):
        return max(self._documents, key=os.path.getmtime)

    def view_document(self) -> str:
        vision = None
        if not self._documents:
            return "Nenhum arquivo encontrado na pasta."

        # Pega o caminho do último documento
        last_doc_path = self._get_last_doc()

        vision = self.__client.chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "system",
                    "content": self._prompt_content,
                },
                {
                    "role": "user",
                    "content": "Oque você está vendo? (RESPONDA EM PORTUGUÊS)",
                    "images": [last_doc_path],  # Envia os dados binários aqui
                },
            ],
        )

        return vision["message"]["content"]
