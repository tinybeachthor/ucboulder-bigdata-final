import arxiv
import os
import pika

def pull_arxiv(client, channel, queue='arxiv'):

    # Search for recent articles
    search = arxiv.Search(
        query="cat:cs.AI",
        max_results = 5,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )
    print(search)

    # Handle results
    results = client.results(search)
    for r in client.results(search):
        print(r.title)
        body = r.title
        channel.basic_publish(exchange='', routing_key=queue, body=body)


if __name__ == '__main__':

    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    queue_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

    # Setup
    client = arxiv.Client()

    params = pika.URLParameters(queue_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='arxiv') # Declare a queue

    # Execute
    pull_arxiv(client, channel)

    # Cleanup
    connection.close()
