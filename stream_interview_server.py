import time
import pika
import os
import openai


class AIAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        self.start_sequence = "\nAIJ:"
        self.restart_sequence = "\nHuman: "
        self.model = "text-davinci-003"
        self.temperature = 1
        self.max_tokens = 4000
        self.top_p = 1
        self.frequency_penalty = 0.62
        self.presence_penalty = 0.6
        self.stop = [" Human:", " AI:"]

        openai.api_key = self.api_key

    def generate_response(self, prompt):
        response = openai.Completion.create(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop
        )
        return response.choices[0].text


class NewsConsumer:
    def __init__(self, host, ai_assistant):
        self.ai_assistant = ai_assistant
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='news_stream')

    def consume(self):
        self.channel.basic_consume(queue='news_stream', on_message_callback=self.callback)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        prompt = body.decode('utf-8').strip() + self.ai_assistant.restart_sequence
        response = self.ai_assistant.generate_response(prompt)
        print(response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        if self.connection.is_open:
            self.connection.close()


if __name__ == '__main__':
    api_key = os.environ.get("OPENAI_API_KEY")
    ai_assistant = AIAssistant(api_key)
    consumer = NewsConsumer('localhost', ai_assistant)
    try:
        consumer.consume()
    except KeyboardInterrupt:
        consumer.close()