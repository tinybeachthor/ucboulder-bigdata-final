import os
import pika

def process_arxiv(ch, method, properties, body):
    print(" [x] Received " + str(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':

    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    # Setup
    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='arxiv') # Declare a queue

    # Execute
    channel.basic_consume('arxiv', process_arxiv, auto_ack=False)

    channel.start_consuming()

    # Cleanup
    connection.close()
