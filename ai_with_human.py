import os

import cv2
import pika
import threading

original_speech_data = []
translated_speech_data = []


# define the RabbitMQ consumer class
class MessageBroker:

    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name
        self.channel = None

    def start_consuming(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=True)
        print(f'Started consuming messages from {self.queue_name} queue...')
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        original_speech = body.decode('utf-8')
        original_speech_data.append(original_speech)


# create instance of RabbitMQ consumer class
original_speech_consumer = MessageBroker('localhost', 'speech_to_text_stream')

# create an instance of the RabbitMQ for the translated speech
translated_speech_consumer = MessageBroker('localhost', 'translated_text_stream')

# start the RabbitMQ consumer thread
original_speech_thread = threading.Thread(target=original_speech_consumer.start_consuming)
original_speech_thread.start()

# start the RabbitMQ consumer thread
translated_speech_thread = threading.Thread(target=translated_speech_consumer.start_consuming)
translated_speech_thread.start()

# start the video stream
cap = cv2.VideoCapture(0)

# set the video frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# set the video frame rate
cap.set(cv2.CAP_PROP_FPS, 60)

while True:
    # read a frame from the video stream
    ret, frame = cap.read()

    # check if the frame is valid
    if not ret:
        break

    # display the recognized text
    if len(original_speech_data) > 0:
        if len(original_speech_data) > 10:
            original_speech_data.pop(0)
            translated_speech_data.pop(0)

        # put the text at the bottom center of the frame and make the font size 12pt and white with border and gray background
        cv2.putText(frame, original_speech_data[-1], (int(frame.shape[1] / 4) - 100, frame.shape[0] - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        # put the translated text at the top center of the frame and make the font size 12pt and white with border and gray background
        cv2.putText(frame, translated_speech_data[-1], (int(frame.shape[1] / 4) - 100, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    else:
        cv2.putText(frame, '.............................', (int(frame.shape[1] / 2) - 100, frame.shape[0] - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    # display the video frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # if c is pressed, then clear the speech data
    if cv2.waitKey(1) & 0xFF == ord('c'):
        original_speech_data.clear()

    # if s is pressed, then save the speech data to a text file
    if cv2.waitKey(1) & 0xFF == ord('s'):
        with open('speech_data_translated.txt', 'w') as f:
            f.write(os.linesep.join(original_speech_data))

# release the video stream and destroy all windows
cap.release()
cv2.destroyAllWindows()

# stop the RabbitMQ consumer thread
original_speech_thread.join()
