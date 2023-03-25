"""
To read video from the webcam using OpenCV in Python, you can use the cv2.VideoCapture() function.
Here's an example code snippet that shows how to read video from the default webcam:
"""

import cv2

# Create a VideoCapture object to read from the webcam
cap = cv2.VideoCapture(0)

# Check if the VideoCapture object was successfully opened
if not cap.isOpened():
    print("Could not open video device")
    exit()

# Loop through the frames in the video
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        print("Could not read frame from video stream")
        break

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # Check if the user pressed the "q" key
    if key == ord('q'):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()

"""
In this code, we create a cv2.VideoCapture() object with the argument 0, 
which tells OpenCV to use the default webcam. 

We then check if the object was successfully opened, and loop through the frames in the video. 
For each frame, we read it using the cap.read() function, display it using cv2.imshow(), 
and wait for a key press using cv2.waitKey(). 

If the user presses the "q" key, we break out of the loop and 
release the VideoCapture object and close the window.
"""