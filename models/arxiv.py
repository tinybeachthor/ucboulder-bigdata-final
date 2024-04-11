from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import json
from enum import StrEnum

from .article import Article as OutputArticle

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

    def safe_id(self):
        return "".join([ c if c.isalnum() else "_" for c in self.id ])

    def to_article(self, audio_url_root):
        return OutputArticle(
                self.id,
                self.id,
                self.title,
                self.authors,
                self.summary,
                audio_url_root+self.safe_id()+".mp3")
