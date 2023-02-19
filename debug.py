def debug(text: str) -> None:
    with open("debug.txt", "a") as file:
        file.write(text + "\n")

def debug_clear() -> None:
    with open("debug.txt", "w") as file:
        file.write("")


