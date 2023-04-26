import os

import cv2
import pika
import threading

import numpy as np
import random

original_speech_data = []
translated_speech_data = []

class Animation:
    """
    This class generates an animation of random shapes on a canvas.
    The animation is displayed in a window and then a text message is added to the last frame.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.shapes = [cv2.circle, cv2.rectangle, cv2.ellipse]
        self.texts = []

    def generate_rectangle(self, pt1=None, pt2=None, color=None, thickness=1):
        """
        This method generates a random rectangle and returns its arguments.
        """
        if pt1 is None:
            pt1 = (random.randint(0, self.width),
                   random.randint(0, self.height))
        
        if pt2 is None:
            pt2 = (random.randint(0, self.width),
                   random.randint(0, self.height))
            
        if color is None:
            color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))

        if thickness is None:
            thickness = random.randint(1, 5)

        return pt1, pt2, color, thickness

    def generate_ellipse(self):
        """
        This method generates a random ellipse and returns its arguments.
        """
        center = (random.randint(0, self.width),
                  random.randint(0, self.height))
        axes = (random.randint(10, 50), random.randint(10, 50))
        angle = random.randint(0, 360)
        start_angle = random.randint(0, 360)
        end_angle = random.randint(0, 360)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        thickness = random.randint(1, 5)
        return center, axes, angle, start_angle, end_angle, color, thickness

    def generate_text(self, text: str):
        """
        This method generates a random text message and returns its arguments.
        """
        org = (random.randint(0, self.width),
               random.randint(0, self.height))
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = random.uniform(1, 4)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        thickness = random.randint(1, 5)
        return text, org, font, font_scale, color, thickness

    def generate_circle(self):
        """
        This method generates a random circle and returns its arguments.
        """
        center = (random.randint(0, self.width),
                  random.randint(0, self.height))
        radius = random.randint(10, 50)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        thickness = random.randint(1, 5)
        return center, radius, color, thickness

    def generate_shape(self):
        """
        This method generates a random shape and returns the shape and its arguments.
        """
        shape = random.choice(self.shapes)
        if shape == cv2.circle:
            return shape, self.generate_circle()
        elif shape == cv2.rectangle:
            return shape, self.generate_rectangle()
        elif shape == cv2.ellipse:
            return shape, self.generate_ellipse()


    def generate_animation(self, num_frames: int, text: str):
        """
        This method generates an animation of random shapes on a canvas.
        """
        for _ in range(num_frames):
            shape, args = self.generate_shape()
            shape(self.canvas, *args)
            cv2.imshow('Animation', self.canvas)
            cv2.waitKey(1)

        # clear canvas before adding the text message
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # generate the sliding text animation
        for _ in range(100):
            self.canvas = np.roll(self.canvas, 10, axis=0)
            self.canvas = np.roll(self.canvas, 10, axis=1)
            cv2.putText(self.canvas, *self.generate_text(text), cv2.LINE_AA)
            cv2.imshow('Animation', self.canvas)
            cv2.waitKey(1)

        # create disappearing text animation by adding boxes as black rectangles
        for _ in range(100):
            # draw a rectangle at a random coordinate on the canvas
            # and add it to the list of rectangles
            cv2.rectangle(self.canvas, *self.generate_rectangle(
                pt1=(random.randint(0, self.width), random.randint(0, self.height)),
                color=(0, 0, 0), thickness=-1
            ))
            cv2.waitKey(1)

        cv2.imshow('Animation', self.canvas)
        cv2.waitKey(0)

    def destroy_animation(self):
        """
        This method destroys the animation window.
        """
        cv2.destroyAllWindows()


# define the RabbitMQ consumer class
class MessageBroker:
    """
    This class is responsible for consuming messages from a RabbitMQ queue.
    """
    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name
        self.channel = None

    def start_consuming(self):
        """
        This method starts consuming messages from the RabbitMQ queue.
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=True)
        print(f'Started consuming messages from {self.queue_name} queue...')
        self.channel.start_consuming()


    def on_message(self, ch, method, properties, body):
        """
        This method is called when a message is received from the RabbitMQ queue.
        """
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

# create an instance of the animation class
animation = Animation(1920, 1080)

# generate random news headlines and place them randomly on the canvas
tech_news = """Last week, the US government announced that it would ban the use of TikTok and WeChat in the country.
The ban will take effect on September 20, 2020.
Twitter has announced that it will ban political ads on its platform.
Facebook has announced that it will ban political ads on its platform.
Google has announced that it will ban political ads on its platform.
TikTok has now been banned in India.
The US government has banned TikTok and WeChat in the country."""

# animation.generate_animation(50, random.choice(tech_news.split('\n')))
# animation.destroy_animation()

while True:
    # read a frame from the video stream
    ret, frame = cap.read()

    # check if the frame is valid
    if not ret:
        break

    ## TODO: check if subscribed speech and translation are available

    # display the recognized text
    if len(original_speech_data) > 1:
        # put the text at the bottom center of the frame and make the font size 12pt and white with border and gray background
        cv2.putText(frame, original_speech_data[-1], (int(frame.shape[1] / 4) - 100, frame.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        # remove the oldest text from the list
        original_speech_data.pop(0)

    else:
        cv2.putText(frame, '.............................', (int(frame.shape[1] / 2) - 100, frame.shape[0] - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    if len(translated_speech_data) > 1:
        # put the translated text at the top center of the frame and make the font size 12pt and white with border and gray background
        cv2.putText(frame, translated_speech_data[-1], (int(frame.shape[1] / 4) - 100, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        translated_speech_data.pop(0)

    else:
        cv2.putText(frame, '.............................', (int(frame.shape[1] / 2) - 100, 40),
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
        with open('speech_data_translated.txt', 'w', encoding="utf-8") as f:
            f.write(os.linesep.join(original_speech_data))

# release the video stream and destroy all windows
cap.release()
cv2.destroyAllWindows()

# stop the RabbitMQ consumer thread
original_speech_thread.join()
