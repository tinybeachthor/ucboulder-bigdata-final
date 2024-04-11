from datetime import datetime
from dateutil import tz

from models.arxiv import Article
from apps.process import process_arxiv

class MockCursor:
    def __init__(self, return_vals=[]):
        self.index = 0
        self.return_vals = return_vals
        self.execute_args = []
    def execute(self, *args):
        self.execute_args.append(args)
    def fetchone(self):
        val = self.return_vals[self.index]
        self.index += 1
        return val
    def fetchall(self):
        val = self.return_vals[self.index]
        self.index += 1
        return val
    def __enter__(self): return self
    def __exit__(*args): pass

class MockConnection:
    def __init__(self, cur):
        self.cur = cur
    def cursor(self):
        return self.cur
    def commit(self): pass

class MockChannel:
    def __init__(self):
        self.basic_ack_args = []
    def basic_ack(self, **kwargs):
        self.basic_ack_args.append(kwargs)

class Method:
    delivery_tag = 0

def mock_tts(article): return article.id


def test_process():
    dt = datetime.now().replace(microsecond=0).astimezone(tz.UTC)
    article = Article("i", dt, "t", ["a", "aa"], "s")

    mock_ch = MockChannel()
    mock_cursor = MockCursor([None])
    mock_conn = MockConnection(mock_cursor)
    args = (mock_conn, mock_tts)

    process_arxiv(mock_ch, Method(), None, article.toJSON().encode(), args)

    assert len(mock_ch.basic_ack_args) == 1
    assert len(mock_cursor.execute_args) == 2

def test_process_exists():
    dt = datetime.now().replace(microsecond=0).astimezone(tz.UTC)
    article = Article("i", dt, "t", ["a", "aa"], "s")

    mock_ch = MockChannel()
    mock_cursor = MockCursor([True])
    mock_conn = MockConnection(mock_cursor)
    args = (mock_conn, mock_tts)

    process_arxiv(mock_ch, Method(), None, article.toJSON().encode(), args)

    assert len(mock_ch.basic_ack_args) == 1
    assert len(mock_cursor.execute_args) == 1

def test_process_invalid():
    mock_ch = MockChannel()
    mock_cursor = MockCursor()
    mock_conn = MockConnection(mock_cursor)
    args = (mock_conn, mock_tts)

    process_arxiv(mock_ch, Method(), None, None, args)

    assert len(mock_ch.basic_ack_args) == 1
    assert len(mock_cursor.execute_args) == 0
