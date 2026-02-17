import emoji
import markdown
from bs4 import BeautifulSoup


class Formatter:
    def __init__(self, text: str = ""):
        self._text: str = text

    def get_formatted_text(self) -> str:
        text = self._text
        # Remove Emojis
        text = emoji.replace_emoji(text, replace="")
        # Convert markdown to HTML
        html = markdown.markdown(text)
        # Use BeautifulSoup to get plain text from HTML
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text()
