from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import json

@dataclass
class Article:
    id: str
    published: datetime
    title: str
    authors: List[str]
    summary: str

    def toJSON(self):
        d = asdict(self)
        d['published'] = self.published.isoformat(timespec='seconds')
        j = json.dumps(d)
        return j
