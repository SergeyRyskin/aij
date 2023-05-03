import os
import time
import cv2
import mediapipe as mp
import cvzone
import numpy as np
import screeninfo

import pandas as pd

import pika
import threading

import openai
from gtts import gTTS
from pygame import mixer

# Using OpenCV to display the image
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
cap.set(cv2.CAP_PROP_FPS, 60)

# initialize dataframe
df = pd.read_csv('news/news.csv', encoding='utf-8')
df = df.dropna()
df = df.reset_index(drop=True)

# text as one line string
titles = ' '.join(df['title'].tolist())

# add '###' between each title
titles = ' ... | '.join(df['title'].tolist())

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

zoomed_text_color = (0, 255, 0)
standard_text_color = (255, 255, 255)
color = standard_text_color

direction = 0
font_size = 12
box_size = 50
news_are_being_played = False


def generate_audio_from_news():
    """
    Convert text to speech and play it
    """
    # initialize tts, create mp3 and play
    tts = gTTS(text=titles, lang='en')
    # save the audio file
    tts.save('news/news.mp3')
    # print the text
    print(
        'The news is: \n' + titles + '\n\n' +
        'The audio file has been saved to news/news.mp3\n\n'
    )


def play_news_from_audio():
    """
    Play the news
    """
    print(
        'Playing the news...\n\n'
    )
    mixer.init()
    mixer.music.load('news/news.mp3')
    mixer.music.play()


def pause_news_from_audio():
    """
    Pauze the news
    """
    mixer.music.pause()


def stop_news_from_audio():
    """
    Stop the news
    """
    mixer.music.stop()


def resume_news_from_audio():
    """
    Resume the news
    """
    mixer.music.unpause()


def rewind_news_from_audio():
    """
    Rewind the news
    """
    mixer.music.rewind()


def forward_news_from_audio():
    """
    Forward the news
    """
    mixer.music.forward()

thread_generate_audio_from_news = threading.Thread(target=generate_audio_from_news)
thread_play_news_from_audio = threading.Thread(target=play_news_from_audio)

# make sure the audio file is generated before playing it
thread_generate_audio_from_news.start()
thread_generate_audio_from_news.join()
thread_play_news_from_audio.start()

# For webcam input:
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
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

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                # if left hand is raised then move the text to the left
                if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.2 and len(results.multi_hand_landmarks) == 1:
                    for i in range(30):
                        # move the text to the left
                        pass
                    titles = titles[1:] + titles[0]
                    direction = 0
                    font_size = 12
                    color = standard_text_color
                    box_size = 50

                # if right hand is raised then move the text to the right
                elif hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > 0.8 and len(results.multi_hand_landmarks) == 1:
                    for i in range(30):
                        # move the text to the left
                        pass
                    direction = 1
                    font_size = 12
                    color = standard_text_color
                    box_size = 50

                # if both hands are raised and all fingers are up then increase the font size to 36pt and change the color
                elif 0.2 < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.8 and len(results.multi_hand_landmarks) == 2 and hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    for i in range(30):
                        # move the text to the left
                        pass
                    font_size = 36
                    color = zoomed_text_color
                    box_size = 100

                # if both hands are raised and all fingers are closed then stop the news
                if 0.2 < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.8 and len(results.multi_hand_landmarks) == 2 and hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    # stop the news
                    pause_news_from_audio()

                # if both hands are raised, thumb and index finger are open then increase the font size to 36pt and change the color
                if 0.2 < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.8 and len(results.multi_hand_landmarks) == 2 and hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y and hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y and hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    # rewind the news
                    resume_news_from_audio()

        else:
            # if no hands are detected then move the text to the left
            font_size = 12
            color = standard_text_color
            box_size = 50

        if direction == 0:
            titles = titles[1:] + titles[0]
        elif direction == 1:
            titles = titles[-1] + titles[:-1]

        # draw the text
        cv2.putText(image, titles, (2, image.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_size / 12, color, 2)

        # put a logo in the top left corner
        logo = cv2.imread('logo.png')

        # resize the logo
        logo = cv2.resize(
            logo, (int(logo.shape[1] / 12), int(logo.shape[0] / 12)))

        # add the logo to the image
        image[0:logo.shape[0], 0:logo.shape[1]] = logo

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('AI News', image)

        # wait for the 'q' key to be pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # if 's' is pressed, save the image
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('news.jpg', image)


# stop the thread that plays the news
thread_play_news_from_audio.join()

# Release the webcam
cap.release()
# Destroy all windows
cv2.destroyAllWindows()
