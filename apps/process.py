import os
import pika

def process_arxiv(ch, method, properties, body):
    print(" [x] Received " + str(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)


def process():
    ARXIV_QUEUE_NAME = "arxiv"

    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    # Setup
    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=ARXIV_QUEUE_NAME)

    # Execute
    channel.basic_consume(ARXIV_QUEUE_NAME, process_arxiv, auto_ack=False)

    channel.start_consuming()

    # Cleanup
    connection.close()
