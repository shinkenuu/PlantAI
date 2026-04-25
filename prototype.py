import logging

from plantai.agents import demeter

logging.basicConfig(level=logging.INFO)


def main() -> None:
    prompt = "Poderosa has yellow leaves. Why is that?"
    demeter.talk(prompt, trace=True)


if __name__ == "__main__":
    main()
