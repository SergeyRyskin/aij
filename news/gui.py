import datetime
import threading
import time

import cv2
import mediapipe as mp
import pika
import screeninfo


class NewsConsumer:
    """
    This class implements a RabbitMQ consumer.
    """
    articles = []
    titles = 'There are no news to display...'

    def __init__(self, host):
        """
        This method initializes the RabbitMQ consumer.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='news_stream')
        self.channel.queue_declare(queue='news_titles')

    def consume(self):
        """
        This method starts consuming messages from the RabbitMQ queue.
        """
        self.channel.basic_consume(queue='news_stream', on_message_callback=self.add_new_article)
        self.channel.basic_consume(queue='news_titles', on_message_callback=self.update_titles)
        self.channel.start_consuming()

    def add_new_article(self, ch, method, properties, body):
        """
        This method adds a new article to the list of articles.
        """
        new_article = body.decode('utf-8')
        # concatenate the new article to the text
        NewsConsumer.articles.append(new_article)

    def update_titles(self, ch, method, properties, body):
        """
        This method updates the titles of the news.
        """
        global titles
        titles = body.decode('utf-8')
        print(
            f"Received titles: {titles} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.titles += titles
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def close(self):
        """
        This method closes the connection to the RabbitMQ server.
        """
        if self.connection.is_open:
            self.connection.close()


def start_consumer():
    """
    This method starts the RabbitMQ consumer.
    """
    consumer = NewsConsumer('localhost')
    try:
        consumer.consume()
    except KeyboardInterrupt:
        consumer.close()


thread = threading.Thread(target=start_consumer)
thread.start()

camera_id = 0


def start_streaming():

    """
    This method starts the video streaming.
    """

    # Using OpenCV to display the image
    cap = cv2.VideoCapture(camera_id)

    w = screeninfo.get_monitors()[0].width
    h = screeninfo.get_monitors()[0].height

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FPS, 60)

    # mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    zoomed_text_color = (0, 255, 0)
    standard_text_color = (255, 255, 255)
    color = standard_text_color

    direction = 0
    font_size = 12
    box_height = 50
    # box width is the same as the image width
    box_width = 1280

    # is_queue_requested = False

    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5) as hands:

        while cap.isOpened():

            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            image = cv2.flip(image, 1)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # create a background for the text with a border
            cv2.rectangle(image, (0, image.shape[0] - box_height), (image.shape[1], image.shape[0]), (0, 0, 0), -1)
            # border
            cv2.rectangle(image, (0, image.shape[0] - box_height), (image.shape[1], image.shape[0]), (255, 255, 255), 2)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    # if left hand is raised then move the text to the left
                    if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.2 and len(results.multi_hand_landmarks) == 1:
                        NewsConsumer.titles = NewsConsumer.titles[1:] + NewsConsumer.titles[0]
                        direction = 0
                        font_size = 12
                        color = standard_text_color
                        box_height = 50

                    # if right hand is raised then move the text to the right
                    elif hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > 0.8 and len(results.multi_hand_landmarks) == 1:
                        direction = 1
                        font_size = 12
                        color = standard_text_color
                        box_height = 50

                    # if both hands are raised then increase the font size to 36pt and change the color
                    elif 0.2 < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.8 and len(results.multi_hand_landmarks) == 2:
                        font_size = 36
                        color = zoomed_text_color
                        box_height = 100

            else:
                # if no hands are detected then move the text to the left
                font_size = 12
                color = standard_text_color
                box_height = 50

            if direction == 0:
                NewsConsumer.titles = NewsConsumer.titles[1:] + NewsConsumer.titles[0]
            elif direction == 1:
                NewsConsumer.titles = NewsConsumer.titles[-1] + NewsConsumer.titles[:-1]

            # draw the text in the bottom left corner with a 2px border in black color. Get the font size from the variable font_size
            cv2.putText(image, NewsConsumer.titles, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, font_size / 12, color, 2, cv2.LINE_AA)

            # draw another text at the right top corner to show the current time of the day in 24h format (HH:MM:SS) and in white color with a 1px border in black color. Change to font-size to 14pt with bold style
            cv2.putText(image, datetime.datetime.now().strftime("%H:%M:%S"), (image.shape[1] - 100, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # put a logo in the top left corner
            logo = cv2.imread('news/logo.png')

            # resize the logo
            # match the size of the logo and time in the top right corner
            logo = cv2.resize(logo, (50, 50))

            # add the logo to the image
            image[0:logo.shape[0], 0:logo.shape[1]] = logo

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('AI News', image)

            # wait for the 'q' key to be pressed
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
                break

            # if 's' is pressed, save the image
            if cv2.waitKey(1) & 0xFF == ord('s') or cv2.waitKey(1) & 0xFF == ord('S'):
                cv2.imwrite('news.jpg', image)

    cap.release()

    # stop the video
    cv2.destroyAllWindows()

    # stop the consumer thread
    thread.join()


def main():
    """
    Main function
    """
    start_streaming()


if __name__ == '__main__':
    main()
