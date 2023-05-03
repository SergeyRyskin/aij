import pika


class NewsConsumer:
    """
    This class implements a RabbitMQ consumer.
    """
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='news_stream')

    def consume(self):
        """
        This method starts consuming messages from the RabbitMQ queue.
        """
        self.channel.basic_consume(queue='news_stream', on_message_callback=self.print_articles)
        self.channel.basic_consume(queue='news_titles', on_message_callback=self.print_titles)
        self.channel.start_consuming()

    def print_articles(self, ch, method, properties, body):
        """
        This method prints the articles.
        """
        print(body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def print_titles(self, ch, method, properties, body):
        """
        This method prints the titles.
        """
        print(body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def destroy(self):
        """
        This method closes the connection to the RabbitMQ server.
        """
        if self.connection.is_open:
            self.connection.close()


if __name__ == '__main__':
    consumer = NewsConsumer('localhost')
    try:
        consumer.consume()
    except KeyboardInterrupt:
        consumer.destroy()
