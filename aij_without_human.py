import cv2
import mediapipe as mp
import cvzone
import numpy as np
import screeninfo

import pandas as pd

import pika
import threading

# Using OpenCV to display the image
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
cap.set(cv2.CAP_PROP_FPS, 60)

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

        # create a background for the text with a border
        cv2.rectangle(image, (0, image.shape[0] - box_size), (image.shape[1], image.shape[0]), (0, 0, 0), -1)
        # border
        cv2.rectangle(image, (0, image.shape[0] - box_size), (image.shape[1], image.shape[0]), (255, 255, 255), 2)


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
                    titles = titles[1:] + titles[0]
                    direction = 0
                    font_size = 12
                    color = standard_text_color
                    box_size = 50

                # if right hand is raised then move the text to the right
                elif hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > 0.8 and len(results.multi_hand_landmarks) == 1:
                    direction = 1
                    font_size = 12
                    color = standard_text_color
                    box_size = 50

                # if both hands are raised then increase the font size to 36pt and change the color
                elif 0.2 < hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.8 and len(results.multi_hand_landmarks) == 2:
                    font_size = 36
                    color = zoomed_text_color
                    box_size = 100

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
        cv2.putText(image, titles, (2, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, font_size / 12, color, 2)

        # put a logo in the top left corner
        logo = cv2.imread('logo.png')

        # resize the logo
        logo = cv2.resize(logo, (int(logo.shape[1] / 12), int(logo.shape[0] / 12)))

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

cap.release()

# stop the video
cv2.destroyAllWindows()
