from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import json
from enum import StrEnum

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

    def fromJSON(j):
        d = json.loads(j)
        published = datetime.fromisoformat(d['published'])
        a = Article(d['id'], published, d['title'], d['authors'], d['summary'])
        return a
