from pathlib import Path
import random


PIC_FOLDER = Path("src/wazowski")
TEXTS_PATH = Path("src/texts.txt")


def get_picture() -> Path:
    pics = list(PIC_FOLDER.glob("*"))
    return random.choice(pics)
    
    
def get_message(additional_text: str = ""):
    texts = TEXTS_PATH.read_text(encoding="utf-8").split("\n")
    text = [random.choice(texts) for _ in range(random.randint(5, 10))]
    text = " ".join(text)
    message = f"азалька! {additional_text}\n\n{text}\n\nтвой ник вазовски"
    return message


if __name__ == "__main__":
    print(get_picture())
    print(get_message())