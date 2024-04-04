import os
import functools
import pika
import psycopg

from models.arxiv import Article as ArxivArticle
from components.database import insert_arxiv

def process_arxiv(ch, method, properties, body, args):
    article = ArxivArticle.fromJSON(body.decode())
    print(article.id)

    conn = args
    with conn.cursor() as cur:
        insert_arxiv(cur, article)
        conn.commit()

    ch.basic_ack(delivery_tag = method.delivery_tag)


def process():
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get(
        'CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    database_url = os.environ.get(
        'DATABASE_URL', 'postgresql://guest:guest@localhost:5432/content')

    # Setup
    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=ARXIV_QUEUE_NAME)

    # Setup database connection
    with psycopg.connect(database_url) as conn:

        # Execute
        callback = functools.partial(process_arxiv, args=(conn))
        channel.basic_consume(ARXIV_QUEUE_NAME, callback, auto_ack=False)

        channel.start_consuming()

    # Cleanup
    connection.close()
