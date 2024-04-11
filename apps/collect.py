import arxiv
import os
import pika
from datetime import datetime
from dateutil import tz
import logging
from pathlib import Path
import tomllib

from models.arxiv import Article as ArxivArticle

log = logging.getLogger(__name__)

TWO_DAYS_MINUTES = 2*24*60

def pull_arxiv(client, channel, queue, category, dt_now):
    log.info('pulling arxiv')

    dt_now = dt_now.astimezone(tz.UTC)

    # Search for recent articles
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results = 1000,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )

    # Handle results
    results = client.results(search)
    for r in client.results(search):
        try:
            log.info(f'got article {r.entry_id}')
            published = r.published.astimezone(tz.UTC)

            # check if recent enough
            age = (dt_now - published).total_seconds() // 60
            log.info(f'article age {age} minutes')
            if (age > TWO_DAYS_MINUTES):
                return

            authors = list(map(str, r.authors))
            article = ArxivArticle(r.entry_id, published, r.title, authors, r.summary)
        except Exception as e:
            log.warning(e)
            continue

        try:
            body = article.toJSON()
            channel.basic_publish(exchange='', routing_key=queue, body=body)
            log.info(f'queued article {r.entry_id}')
        except Exception as e:
            log.warning(e)
            continue


def collect(production=False):
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    categories_path = Path(os.getcwd()) / "config" / "arxiv_categories.toml"
    if production:
        with open(categories_path, "rb") as f:
            categories = tomllib.load(f).keys()
    else:
        categories = ['cs.AI', 'cs.RO']

    log.info(f'categories: {categories}')

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

    now = datetime.now()
    log.info(f'time now is {now}')

    for category in categories:
        log.info(f'pull arxiv category {category}')
        pull_arxiv(client, channel,
            queue = ARXIV_QUEUE_NAME,
            category = category,
            dt_now = now)

    log.info('execute done')

    # Cleanup
    connection.close()
