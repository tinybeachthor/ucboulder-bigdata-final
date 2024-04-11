from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Article:
    id: str
    link: str
    title: str
    authors: List[str]
    summary: str
    audio_url: str

    def toJSON(self):
        d = asdict(self)
        j = json.dumps(d)
        return j
