import pika

# connect to RabbitMQ message broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create message queue
channel.queue_declare(queue='voice_data')


# function to consume messages from message queue
def callback(ch, method, properties, body):
    print(f"Received recognized text: {body.decode()}")


# start consuming messages from message queue
channel.basic_consume(queue='voice_data', on_message_callback=callback, auto_ack=True)
print('Waiting for recognized text messages...')
channel.start_consuming()
