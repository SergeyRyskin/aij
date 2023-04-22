from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from glob import glob

import cv2
from deepface import DeepFace
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


backends = [
    "opencv",
    "ssd",
    "dlib",
    "mtcnn",
    "retinaface",
    "mediapipe"
]

default_backend = backends[0]

models = [
    "VGG-Face",
    "Facenet",
    "Facenet512",
    "OpenFace",
    "DeepFace",
    "DeepID",
    "ArcFace",
    "Dlib",
    "SFace",
]

default_model = models[0];

face_attributes = DeepFace.analyze(
    img_path="deep_face_db/scarlett johansson/scarlett05.png",
    detector_backend="opencv",
    align=True
)

# print the attributes
for attribute in face_attributes[0].keys():
    print(attribute)

# print the dominant emotion
print(face_attributes[0]['dominant_emotion'])



imgs = glob("deep_face_db/yilmaz mustafa/*")

for img in imgs:

    try:

        emdf = DeepFace.analyze(img_path=img, actions=['emotion'], detector_backend="opencv", align=True)

        # Get the emotion data from the dictionary
        emotion_data = emdf[0]['emotion']

        # convert to dataframe
        emotion_df = pd.DataFrame(emotion_data, index=[0])

        fig, axs = plt.subplots(1, 2, figsize=(15, 10))
        axs[0].imshow(cv2.imread(img)[:, :, ::-1])
        axs[0].set_title("Yilmaz Mustafa \n(path: " + img + ")")
        axs[0].axis('off')

        axs[1].bar(emotion_df.columns, emotion_df.iloc[0])
        axs[1].set_title("Emotion Analysis")
        axs[1].set_xlabel("Emotion")

        plt.tight_layout()

        plt.show()


    except:
        print("error occurred, possibly no face detected")


default_backend = "opencv"
default_model = "Facenet"

cam = cv2.VideoCapture(0)

# set the resolution of the camera to full screen size
# get the width and height of the screen
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# set the width and height, and UNSUCCESSFULLY set the exposure time
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 60)

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)  # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    try:

        # predict the emotion
        emotion = DeepFace.analyze(img_path=img, actions=['emotion'], detector_backend=default_backend, align=True, silent=True)

        # get the emotion data from the dictionary
        emotion_data = emotion[0]['emotion']

        # convert to dataframe
        emotion_df = pd.DataFrame(emotion_data, index=[0])

        # get the dominant emotion
        emotion_label = emotion_df.idxmax(axis=1)[0]

        # draw the emotion label at the bottom of the frame and display it such as "Happy: 0.99, Sad: 0.01"
        cv2.putText(img, emotion_label + ": " + str(emotion_df[emotion_label][0]), (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # if the emotion is happy, then draw a green rectangle around the face
        if emotion_label == "happy":
            cv2.rectangle(img, (int(minW), int(minH)), (int(width - minW), int(height - minH)), (0, 255, 0), 2)

        # if the emotion is sad, then draw a red rectangle around the face
        if emotion_label == "sad":
            cv2.rectangle(img, (int(minW), int(minH)), (int(width - minW), int(height - minH)), (0, 0, 255), 2)

        # if the emotion is angry, then draw a blue rectangle around the face
        if emotion_label == "angry":
            cv2.rectangle(img, (int(minW), int(minH)), (int(width - minW), int(height - minH)), (255, 0, 0), 2)

        # if the emotion is neutral, then draw a yellow rectangle around the face
        if emotion_label == "neutral":
            cv2.rectangle(img, (int(minW), int(minH)), (int(width - minW), int(height - minH)), (0, 255, 255), 2)

    except:
        # draw error message if no face detected
        cv2.putText(img, "No face detected", (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # show the frame
    cv2.imshow('Emotion Recognition', img)

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
