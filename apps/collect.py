import arxiv
import os
import pika
from datetime import datetime
from dateutil import tz

from models.arxiv import Article as ArxivArticle

def pull_arxiv(client, channel, queue):

    # Search for recent articles
    search = arxiv.Search(
        query="cat:cs.AI",
        max_results = 5,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )

    # Handle results
    results = client.results(search)
    for r in client.results(search):

        published = r.published.astimezone(tz.UTC)
        authors = list(map(str, r.authors))
        article = ArxivArticle(r.entry_id, published, r.title, authors, r.summary)

        body = article.toJSON()
        channel.basic_publish(exchange='', routing_key=queue, body=body)


def collect():
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    # Setup
    client = arxiv.Client()

    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare queues
    channel.queue_declare(queue=ARXIV_QUEUE_NAME)

    # Execute
    pull_arxiv(client, channel, queue=ARXIV_QUEUE_NAME)

    # Cleanup
    connection.close()
