import speech_recognition

# r = speech_recognition.Recognizer()

# with speech_recognition.Microphone() as source:
#     print("Escutando...")
#     audio = r.listen(source)

# text = r.recognize_google(audio, language="pt-BR")
# print(text)


class STT:
    def __init__(self):
        self._recognizer = speech_recognition.Recognizer()

    def _listen(self) -> speech_recognition.AudioData | None:
        with speech_recognition.Microphone() as source:
            # 1. Calibração mais rápida para não perder o início da fala
            self._recognizer.adjust_for_ambient_noise(source, duration=0.3)

            # 2. Sensibilidade ao silêncio (O segredo está aqui)
            # Aumenta o tempo de silêncio necessário para considerar que você parou de falar
            self._recognizer.pause_threshold = (
                2.0  # Padrão é 0.8, aumentamos para 2 segundos
            )
            self._recognizer.non_speaking_duration = 1.0  # Mantém o buffer de áudio

            print("Luna está escutando (pode falar frases longas)...")
            try:
                audio = self._recognizer.listen(
                    source,
                    timeout=None,  # Espera indefinidamente até você começar a falar
                    phrase_time_limit=None,  # NÃO corta por tempo, ouve até você terminar
                )
                return audio
            except Exception as e:
                print(f"Erro na captura: {e}")
                return None

    def get_text(self) -> str:
        audio = self._listen()
        if not audio:
            return ""
        try:
            text = self._recognizer.recognize_google(audio, language="pt-BR")
            return text
        except speech_recognition.UnknownValueError:
            return ""
        except speech_recognition.RequestError:
            print("Luna não encontrou seu microfone...")
            return ""
