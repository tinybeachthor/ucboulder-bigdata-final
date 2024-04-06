import os
from pathlib import Path
import functools
import pika
import psycopg
import logging

from models.arxiv import Article as ArxivArticle
from components.database import exists_arxiv, insert_arxiv
from components.text import TextUtil
from components.text2speech import MockTTS

log = logging.getLogger(__name__)

def process_arxiv(ch, method, properties, body, args):
    conn, production, dirpath, text_util, tts = args

    # parse
    try:
        article = ArxivArticle.fromJSON(body.decode())
        log.info(f'process_arxiv {article.id}')
    except Exception as e:
        log.warn(e)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    # check if already exists in database
    with conn.cursor() as cur:
        if exists_arxiv(cur, article.id):
            log.info(f'already in database {article.id}')
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return

    # text2speech
    try:
        sentences = text_util.split_sentences(article.summary)
        # in dev, only use title to keep processing time low
        if production:
            sentences = [article.title] + sentences
        else:
            sentences = [article.title]
        filepath = dirpath / article.safe_id()
        tts.generate(sentences, filepath)

    except Exception as e:
        log.warn(e)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    # upload audio to object store

    # insert to database
    with conn.cursor() as cur:
        insert_arxiv(cur, article)
        conn.commit()

    log.info(f'process_arxiv done {article.id}')
    ch.basic_ack(delivery_tag = method.delivery_tag)


def process(production=False):
    ARXIV_QUEUE_NAME = "arxiv"
    WORK_DIR = Path(os.getcwd()) / ".tmp" / "process"

    os.makedirs(WORK_DIR, exist_ok=True)

    queue_url = os.environ.get(
        'CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
    database_url = os.environ.get(
        'DATABASE_URL', 'postgresql://guest:guest@localhost:5432/content')

    # Setup
    log.info('setup start')

    text_util = TextUtil()
    tts = MockTTS()

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
        args = (conn, production, WORK_DIR, text_util, tts)
        callback = functools.partial(process_arxiv, args=args)
        channel.basic_consume(ARXIV_QUEUE_NAME, callback, auto_ack=False)

        channel.start_consuming()

    log.info('execute done')

    # Cleanup
    connection.close()
