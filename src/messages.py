from pathlib import Path
import random
from typing import List


PIC_FOLDER = Path("src/wazowski")
TEXTS_PATH = Path("src/texts")
MINAPOVA_NAMES = [
    "азалька", "минаша",
    "азаля", "азаличка",
    "солнышко", "миналия азапова",
    "азалия раисовна", "малышка"
]


def extract_random_text(path: Path, amount: int, separator: str = " ") -> str:
    texts = path.read_text(encoding="utf-8").split("\n")
    texts = random.sample(texts, amount)
    return separator.join(texts)


def get_picture() -> Path:
    pics = list(PIC_FOLDER.glob("*"))
    return random.choice(pics)


def get_message(additional_text: str = ""):
    text = extract_random_text(TEXTS_PATH / "basic.txt", random.randint(5, 10))
    name = random.choice(MINAPOVA_NAMES)
    message = f"{name}!\n\n{additional_text}\n\nи не забывай, что {text}\n\nтвой ник вазовски"
    return message


if __name__ == "__main__":
    print(get_picture())
    print(get_message())
