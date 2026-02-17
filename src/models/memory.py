from src.models.soul import Soul


class Memory:
    def __init__(self):
        soul: Soul = Soul()
        self.__prompt: map[str, str] = {
            "role": "system",
            "content": soul.live(),
        }
        self.__chat_memory: list[map[str, str]] = [self.__prompt]

    def add_user_message(self, message: str) -> None:
        self.__chat_memory.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistent_response(self, response: str) -> None:
        self.__chat_memory.append(
            {
                "role": "assistent",
                "content": response,
            }
        )

    def get_memory(self) -> list[str, str]:
        return self.__chat_memory
