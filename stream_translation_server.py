import pika
import os
import deepl


class RabbitMQTranslator:
    def __init__(self, input_queue_name, output_queue_name, rabbitmq_host='localhost'):
        self.rabbitmq_host = rabbitmq_host
        self.input_queue_name = input_queue_name
        self.output_queue_name = output_queue_name
        self.api_key = os.environ.get('DEEPL_AUTH_KEY')

        self.input_channel = None
        self.output_channel = None

        self.connection = None
        self.connect()

    def connect(self):
        parameters = pika.ConnectionParameters(host=self.rabbitmq_host)
        self.connection = pika.BlockingConnection(parameters)

        self.input_channel = self.connection.channel()
        self.input_channel.queue_declare(queue=self.input_queue_name)

        self.output_channel = self.connection.channel()
        self.output_channel.queue_declare(queue=self.output_queue_name)

    def start_consuming(self):
        self.input_channel.basic_consume(queue=self.input_queue_name, on_message_callback=self.on_message,
                                         auto_ack=True)
        self.input_channel.start_consuming()

    def on_message(self, channel, method, properties, body):
        message_text = body.decode('utf-8')
        translated_text = self.translate(message_text)
        self.send_message(translated_text)

    def translate(self, text):
        translator = deepl.Translator(self.api_key)
        translated_text = translator.translate_text(text, source_lang='EN', target_lang='NL').text
        return translated_text

    def send_message(self, message):
        self.output_channel.basic_publish(exchange='', routing_key=self.output_queue_name, body=message)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    translator = RabbitMQTranslator('voice_data', 'translation_data')
    translator.start_consuming()
