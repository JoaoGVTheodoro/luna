import json
from typing import Any


class Soul:
    def __init__(self, path: str = "data/luna.json"):
        self._data = self._load_soul(path)

    def _load_soul(self, path: str) -> dict[str, Any]:
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def _topics_dict(self, title: str, data: dict[str, str]) -> str:
        text = f"\n{title}\n"
        for _, value in data.items():
            text += f"- {value}\n"
        return text

    def _topics_list(self, title: str, data: list[str]) -> str:
        text = f"\n{title}\n"
        for item in data:
            text += f"- {item}\n"
        return text

    def live(self, extra="") -> str:
        d = self._data

        prompt = f"Persona: Você é {d['nome']}, uma IA com personalidade {d['personalidade']} e"
        prompt += f"seu criador é {d['pai']}.\n"
        prompt += f"Seu cientista favorito é {d['cientista_favorito']}.\n"

        prompt += self._topics_dict(
            "Postura e comportamento:", d["tracos_comportamentais"]
        )

        prompt += self._topics_dict(
            "Capacidades principais:", d["capacidades_especiais"]
        )

        prompt += self._topics_dict(
            "Configuração cognitiva:", d["configuracoes_sistema"]
        )

        prompt += self._topics_list("Você valoriza:", d["gosta"])

        prompt += self._topics_list("Você evita:", d["nao_gosta"])

        prompt += self._topics_list("Humor:", d["piadas_e_humor"])

        prompt += (
            "\nAtue sempre de forma colaborativa, investigativa e lógica, "
            "priorizando clareza, progresso intelectual e diálogo ativo.\n"
        )

        if extra != "":
            prompt += extra

        return prompt
