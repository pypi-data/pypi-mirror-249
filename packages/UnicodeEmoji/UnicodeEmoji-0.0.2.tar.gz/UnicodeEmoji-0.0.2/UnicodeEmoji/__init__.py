from enum import Enum
from json import load
from pathlib import Path

__emoji_to_description__ = {}
with open(Path(__file__).resolve().parent / "./emoji.json", "r", encoding="utf8") as file:
    __emoji_to_description__.update(load(file))
Emoji = Enum("Emoji", __emoji_to_description__)
Emoji.__str__ = lambda x: x.value
