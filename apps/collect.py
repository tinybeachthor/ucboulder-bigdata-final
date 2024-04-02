import arxiv
import os
import pika
from datetime import datetime
from dateutil import tz
import logging

from models.arxiv import Article as ArxivArticle

log = logging.getLogger(__name__)

def pull_arxiv(client, channel, queue):
    log.info('pulling arxiv')

    # Search for recent articles
    search = arxiv.Search(
        query="cat:cs.AI",
        max_results = 5,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )

    # Handle results
    results = client.results(search)
    for r in client.results(search):
        try:
            log.info(f'got article {r.entry_id}')
            published = r.published.astimezone(tz.UTC)
            authors = list(map(str, r.authors))
            article = ArxivArticle(r.entry_id, published, r.title, authors, r.summary)
        except Exception as e:
            log.warn(e)
            continue

        try:
            body = article.toJSON()
            channel.basic_publish(exchange='', routing_key=queue, body=body)
            log.info(f'queued article {r.entry_id}')
        except Exception as e:
            log.warn(e)
            continue


def collect():
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    # Setup
    log.info('setup start')
    client = arxiv.Client()

    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare queues
    channel.queue_declare(queue=ARXIV_QUEUE_NAME)

    log.info('setup done')

    # Execute
    log.info('execute start')

    pull_arxiv(client, channel, queue=ARXIV_QUEUE_NAME)

    log.info('execute done')

    # Cleanup
    connection.close()
