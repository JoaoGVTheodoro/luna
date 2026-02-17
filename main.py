from src.models.luna import Luna


class Main:
    def run(self):
        luna = Luna(
            model="llama3.1:8b",
            online=True,
        )
        while True:
            message = input("\033[32m>> \033[m")

            if message:
                luna.get_response(message)


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt:
        print("Programa finalizdo")
