import os
import time
import edge_tts
import asyncio
import pygame

from src.utils.formatter import Formatter


class TTS:
    def __init__(self, voice):
        self._voice = voice

    async def _generate_audio(self, text: str, file: str = "say.mp3") -> None:
        comunicate = edge_tts.Communicate(text, self._voice)
        await comunicate.save(file)

    def _delete_file(self, file: str) -> None:
        if os.path.exists(file):
            os.remove(file)

    def say(self, text: str, file: str) -> None:
        start_time = time.time()  # Início do cálculo

        formatter = Formatter(text)
        formatted_text = formatter.get_formatted_text()

        asyncio.run(self._generate_audio(formatted_text, file))

        pygame.mixer.init()
        sound_effect = pygame.mixer.Sound(file)

        # O play() retorna um objeto Channel
        channel = sound_effect.play()

        # Bloqueia o código enquanto o áudio estiver tocando
        while channel.get_busy():
            time.sleep(0.1)

        end_time = time.time()  # Fim do cálculo
        duration = end_time - start_time

        print(f"Tempo total (Geração + Fala): {duration:.2f} segundos")

        # Garante que o arquivo não está sendo usado antes de deletar
        pygame.mixer.quit()
        self._delete_file(file)
