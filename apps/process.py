import os
from pathlib import Path
import functools
import pika
import psycopg
import logging
import boto3
from botocore.exceptions import ClientError

from models.arxiv import Article as ArxivArticle
from components.database import exists_arxiv, insert_arxiv
from components.text import TextUtil
from components.text2speech import TTS

log = logging.getLogger(__name__)

def tts_upload(article,
               tts = TTS(), text_util = TextUtil(), workdir = os.getcwd(),
               production = True, s3 = None, s3_bucket = None):

    filename = article.safe_id() + ".mp3"
    filepath = workdir / filename

    sentences = text_util.split_sentences(article.summary)
    # in dev, only use title to keep processing time low
    if production:
        sentences = [article.title] + sentences
    else:
        sentences = [article.title]

    tts.generate(sentences, filepath)

    # upload audio to object store
    if s3:
        s3.upload_file(filepath, s3_bucket, filename)

    return filepath


def process_arxiv(ch, method, properties, body, args):
    conn, run_tts_upload = args

    # parse
    try:
        article = ArxivArticle.fromJSON(body.decode())
        log.info(f'process_arxiv {article.id}')
    except Exception as e:
        log.warning(e)
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
        filepath = run_tts_upload(article)
    except ClientError as e:
        log.error(e)
        return
    except Exception as e:
        log.warning(e)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    if os.path.exists(filepath):
        os.remove(filepath)

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

    s3_endpoint = os.environ.get('S3_ENDPOINT', 'http://localhost:4566')
    s3_access_key = os.environ.get('S3_ACCESS_KEY', 'test')
    s3_secret_key = os.environ.get('S3_SECRET_KEY', 'test')
    s3_region = os.environ.get('S3_REGION', 'us-west-1')
    s3_bucket = os.environ.get('S3_BUCKET', 'objects')

    # Setup
    log.info('setup start')

    text_util = TextUtil()
    tts = TTS()

    s3 = boto3.client(
            service_name = "s3",
            endpoint_url = s3_endpoint,
            aws_access_key_id = s3_access_key,
            aws_secret_access_key = s3_secret_key,
            region_name = s3_region)

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
        run_tts_upload = functools.partial(
                tts_upload, tts=tts, text_util=text_util, workdir=WORK_DIR,
                production=production, s3=s3, s3_bucket=s3_bucket)
        args = (conn, run_tts_upload)
        callback = functools.partial(process_arxiv, args=args)
        channel.basic_consume(ARXIV_QUEUE_NAME, callback, auto_ack=False)

        channel.start_consuming()

    log.info('execute done')

    # Cleanup
    connection.close()
