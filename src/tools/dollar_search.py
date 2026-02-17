import requests


class DollarSearch:
    def __init__(self, from_coin: str = "USD", to_coin: str = "BRL"):
        self._url = (
            f"https://economia.awesomeapi.com.br/json/last/{from_coin}-{to_coin}"
        )
        self._from = from_coin
        self._to = to_coin

    def search(self):
        response = requests.get(self._url)
        search_response = ""

        if response.status_code >= 400:
            search_response = "Desculpe, mas não encontrei a cotação informada."

        if response.status_code == 200:
            data = response.json()[f"{self._from}{self._to}"]
            search_response = "Luna organize esses dados de cotação:\n"
            search_response += f"- Moéda original: {data["codein"]}\n"
            search_response += f"- Moéda de origem: {data["high"]}\n"
            search_response += f"- Data de busca: {data["create_date"]}\n"
            search_response += f"Breve descrição: {data["name"]}"

        return search_response
