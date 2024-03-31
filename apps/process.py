import os
import functools
import pika
import psycopg

from models.arxiv import Article as ArxivArticle

def process_arxiv(ch, method, properties, body, args):
    article = ArxivArticle.fromJSON(body.decode())
    print(article.id)

    aid = article.id
    published = article.published
    title = article.title
    authors = "; ".join(article.authors)
    summary = article.summary

    conn = args
    with conn.cursor() as cur:

        cur.execute(
            "insert into ARXIV (id, published, title, authors, summary) \
             values (%s, %s, %s, %s, %s) \
             on conflict do nothing",
            (aid, published, title, authors, summary))

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
