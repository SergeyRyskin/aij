"""
In this code, we defined a MessageBroker class that encapsulates the functionality of connecting to a message broker, creating a channel, and consuming messages from a queue. We also defined a handle_message function to handle messages consumed from the queue. The main function creates an instance of the MessageBroker class, connects to the message broker, and starts consuming messages from the queue using the handle_message function. We added a KeyboardInterrupt exception handler to catch the user pressing Ctrl+C and close the connection to the message broker.
"""

import pika


class TranslationClient:
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='translated_text_stream')

    def consume(self, callback):
        self.channel.basic_consume(queue='translated_text_stream', on_message_callback=callback, auto_ack=True)
        print('Waiting for recognized text messages...')
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection is not None and not self.connection.is_closed:
            self.connection.close()


# function to consume messages from message queue
def handle_message(ch, method, properties, body):
    print(body.decode('utf-8'))


def main():
    message_broker = TranslationClient('localhost')
    message_broker.connect()
    try:
        message_broker.consume(handle_message)
    except KeyboardInterrupt:
        message_broker.close_connection()
        print('Connection to message broker closed.')


if __name__ == '__main__':
    main()
