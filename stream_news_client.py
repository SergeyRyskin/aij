import time

import pika

# connect to RabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create message queue
channel.queue_declare(queue='news_stream')


def callback(ch, method, properties, body):
    # print the news dataset
    print(
        """
--------------------------------------------------------------------------------
Published news from {source} to the news_stream queue. 
The body of the message is the news dataset in JSON format.
--------------------------------------------------------------------------------
{body}
--------------------------------------------------------------------------------
""".format(source=method.routing_key, body=body.decode('utf-8'))
    )

    # acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# consume the news dataset from the news_top_headlines_stream queue
channel.basic_consume(queue='news_stream', on_message_callback=callback)

# start consuming
channel.start_consuming()

# close the connection
if connection.is_open:
    connection.close()
