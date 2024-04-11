from dataclasses import dataclass
from typing import List

@dataclass
class Article:
    id: str
    link: str
    title: str
    authors: List[str]
    summary: str
    audio_url: str
