from datetime import datetime
from dateutil import tz
from arxiv import Result

from models.arxiv import Article
from apps.collect import pull_arxiv

# Testing the integration between:
# - collect job
# - message queue


class MockClient:
    def __init__(self, results):
        self.results_return = results
    def results(self, search):
        return self.results_return

class MockChannel:
    def __init__(self):
        self.basic_publish_args = []
    def basic_publish(self, **kwargs):
        self.basic_publish_args.append(kwargs)


def test_empty():
    mock_client = MockClient([])
    mock_channel = MockChannel()
    queue = "test_arxiv"
    cat = "cs.AI"
    now = datetime.now().replace(microsecond=0).astimezone(tz.UTC)

    pull_arxiv(mock_client, mock_channel, queue, cat, now)

    assert len(mock_channel.basic_publish_args) == 0

def test_single():
    dt = datetime.now().replace(microsecond=0).astimezone(tz.UTC)
    article = Article("i", dt, "t", ["a", "aa"], "s")
    article_raw = Result(
        article.id,
        published = article.published,
        title = article.title,
        summary = article.summary,
        authors = list(map(Result.Author, article.authors)))

    mock_client = MockClient([article_raw])
    mock_channel = MockChannel()
    queue = "test_arxiv"
    cat = "cs.AI"

    pull_arxiv(mock_client, mock_channel, queue, cat, dt)

    assert len(mock_channel.basic_publish_args) == 1
    assert mock_channel.basic_publish_args[0]['routing_key'] == queue
    assert mock_channel.basic_publish_args[0]['exchange'] == ''
    assert mock_channel.basic_publish_args[0]['body'] == article.toJSON()

def test_multiple():
    dt = datetime.now().replace(microsecond=0).astimezone(tz.UTC)
    article = Article("i", dt, "t", ["a", "aa"], "s")
    article_raw = Result(
        article.id,
        published = article.published,
        title = article.title,
        summary = article.summary,
        authors = list(map(Result.Author, article.authors)))

    mock_client = MockClient([article_raw, article_raw])
    mock_channel = MockChannel()
    queue = "test_arxiv"
    cat = "cs.AI"

    pull_arxiv(mock_client, mock_channel, queue, cat, dt)

    assert len(mock_channel.basic_publish_args) == 2
    assert mock_channel.basic_publish_args[0]['routing_key'] == queue
    assert mock_channel.basic_publish_args[0]['exchange'] == ''
    assert mock_channel.basic_publish_args[0]['body'] == article.toJSON()
    assert mock_channel.basic_publish_args[1]['routing_key'] == queue
    assert mock_channel.basic_publish_args[1]['exchange'] == ''
    assert mock_channel.basic_publish_args[1]['body'] == article.toJSON()

def test_old():
    now = datetime.now().replace(microsecond=0).astimezone(tz.UTC)
    dt = now.replace(year=1999)
    article = Article("i", dt, "t", ["a", "aa"], "s")
    article_raw = Result(
        article.id,
        published = article.published,
        title = article.title,
        summary = article.summary,
        authors = list(map(Result.Author, article.authors)))

    mock_client = MockClient([article_raw, article_raw])
    mock_channel = MockChannel()
    queue = "test_arxiv"
    cat = "cs.AI"

    pull_arxiv(mock_client, mock_channel, queue, cat, now)

    assert len(mock_channel.basic_publish_args) == 0
