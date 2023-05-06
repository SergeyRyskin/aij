import cv2
import os
import random
import numpy as np
import pandas as pd

user_profile = os.environ['USERPROFILE']
SEP = os.path.sep

# Path to the album directory containing all the images
image_home = user_profile + SEP + '.aij' + SEP + 'image'
album_path = image_home + SEP + 'intro'

# List all files in the directory
files = os.listdir(album_path)

# Load all the images
images = []
for file in files:
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
        img = cv2.imread(os.path.join(album_path, file))
        images.append(img)

# Shuffle the images
random.shuffle(images)

# Define the animation parameters
animation_width = 800
animation_height = 600
fps = 30
duration = 10 # in seconds

# Create the video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('animation.mp4', fourcc, fps, (animation_width, animation_height))

# Define the initial position of the first image
x = 0
y = 0

# Generate the animation frames
num_frames = fps * duration
for i in range(num_frames):
    # Create a blank frame
    frame = np.zeros((animation_height, animation_width, 3), dtype=np.uint8)
    
    # Choose a random image and resize it to a random size
    img = random.choice(images)
    scale = random.uniform(0.2, 1.0)
    img = cv2.resize(img, None, fx=scale, fy=scale)
    
    # Update the image position
    x += random.randint(-50, 50)
    y += random.randint(-50, 50)
    x = max(0, min(x, animation_width - img.shape[1]))
    y = max(0, min(y, animation_height - img.shape[0]))
    
    # Check if the image dimensions exceed the frame dimensions
    if img.shape[0] > animation_height:
        img = img[:animation_height, :, :]
    if img.shape[1] > animation_width:
        img = img[:, :animation_width, :]
    
    # Draw the image on the frame
    img_height, img_width, _ = img.shape
    frame[y:y+img_height, x:x+img_width] = img
    
    # Write the frame to the video writer
    video_writer.write(frame)

# Release the video writer and destroy all windows
video_writer.release()
cv2.destroyAllWindows()
