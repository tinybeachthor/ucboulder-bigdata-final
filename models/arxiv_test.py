from datetime import datetime

from .arxiv import Article

def test_json_encode():
    d = datetime.now()
    dj = d.isoformat(timespec='seconds')

    a = Article("i", d, "t", ["a", "aa"], "s")
    j = a.toJSON()

    expected = '{'
    expected += '"id": "i", '
    expected += '"published": "'+dj+'", '
    expected += '"title": "t", '
    expected += '"authors": ["a", "aa"], '
    expected += '"summary": "s"'
    expected += '}'

    assert j == expected
