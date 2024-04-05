import os
import functools
import pika
import psycopg
import logging

from models.arxiv import Article as ArxivArticle
from components.database import insert_arxiv

log = logging.getLogger(__name__)

def process_arxiv(ch, method, properties, body, args):
    try:
        article = ArxivArticle.fromJSON(body.decode())
        log.info('process_arxiv', article.id)
    except Exception as e:
        log.warn(e)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    conn = args
    with conn.cursor() as cur:
        insert_arxiv(cur, article)
        conn.commit()

    log.info('process_arxiv done', article.id)
    ch.basic_ack(delivery_tag = method.delivery_tag)


def process():
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get(
        'CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    database_url = os.environ.get(
        'DATABASE_URL', 'postgresql://guest:guest@localhost:5432/content')

    # Setup
    log.info('setup start')

    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=ARXIV_QUEUE_NAME)

    log.info('setup done')

    # Setup database connection
    log.info('execute start')

    with psycopg.connect(database_url) as conn:

        # Execute
        callback = functools.partial(process_arxiv, args=(conn))
        channel.basic_consume(ARXIV_QUEUE_NAME, callback, auto_ack=False)

        channel.start_consuming()

    log.info('execute done')

    # Cleanup
    connection.close()
