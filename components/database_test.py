from datetime import datetime

from models.arxiv import Article
from .database import exists_arxiv, insert_arxiv, get_arxiv_latest

class MockCursor:
    def __init__(self, return_val=None):
        self.return_val = return_val
    def execute(self, *args):
        self.execute_args = args
    def fetchone(self):
        return self.return_val
    def fetchall(self):
        return self.return_val


def test_exists_arxiv():
    mock_cur = MockCursor("row")
    assert exists_arxiv(mock_cur, "id")

def test_exists_arxiv_none():
    mock_cur = MockCursor(None)
    assert not exists_arxiv(mock_cur, "id")

def test_insert_arxiv():
    d = datetime.now().replace(microsecond=0)
    article = Article("id", d, "t", ["a", "aa"], "s")

    mock_cur = MockCursor()
    insert_arxiv(mock_cur, article)

    assert len(mock_cur.execute_args) == 2
    assert len(mock_cur.execute_args[1]) == 5
    assert mock_cur.execute_args[1][0] == "id"
    assert mock_cur.execute_args[1][1] == d
    assert mock_cur.execute_args[1][2] == "t"
    assert mock_cur.execute_args[1][3] == "a; aa"
    assert mock_cur.execute_args[1][4] == "s"

def test_get_arxiv_latest():
    d = datetime.now().replace(microsecond=0)
    article = Article("id", d, "t", ["a", "aa"], "s")

    raw = {}
    raw[0] = "id"
    raw[1] = d
    raw[2] = "t"
    raw[3] = "a; aa"
    raw[4] = "s"

    mock_cur = MockCursor([raw])

    assert get_arxiv_latest(mock_cur) == [article]

def test_get_arxiv_latest_limit():
    mock_cur = MockCursor([])

    get_arxiv_latest(mock_cur, limit=42)

    assert mock_cur.execute_args[1][0] == 42
