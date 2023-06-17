import cv2 as cv 
import numpy as np
from keras.models import load_model

# Load the model.
model = load_model("Documents\AA Uni\Year 3\Robotics\Assignment 3\\CNN_model.h5")

# Get the webcam feed.
cap = cv.VideoCapture(0)

# Set the resolution of the camera.
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# Turn class label to class title
def class_label(cnum):
    #if   cnum == 0: return "Speed Limit 20 km/h"
    #elif cnum == 1: return "Speed Limit 30 km/h"
    if cnum == 0: return "Speed Limit 50 km/h"
    #elif cnum == 3: return "Speed Limit 60 km/h"
    #elif cnum == 4: return "Speed Limit 70 km/h"
    #elif cnum == 5: return "Speed Limit 80 km/h"
    #elif cnum == 6: return "End of Speed Limit 80 km/h"
    elif cnum == 1: return "Speed Limit 100 km/h"
    # elif cnum == 8: return "Speed Limit 120 km/h"
    # elif cnum == 9: return "No passing"
    # elif cnum == 10: return "No passing for vechiles over 3.5 metric tons"
    # elif cnum == 11: return "Right-of-way at the next intersection"
    # elif cnum == 12: return "Priority road"
    # elif cnum == 13: return "Yield"
    elif cnum == 2: return "Stop"
    # elif cnum == 15: return "No vechiles"
    # elif cnum == 16: return "Vechiles over 3.5 metric tons prohibited"
    elif cnum == 3: return "No entry"
    # elif cnum == 18: return "General caution"
    # elif cnum == 19: return "Dangerous curve to the left"
    # elif cnum == 20: return "Dangerous curve to the right"
    # elif cnum == 21: return "Double curve"
    # elif cnum == 22: return "Bumpy road"
    # elif cnum == 23: return "Slippery road"
    # elif cnum == 24: return "Road narrows on the right"
    # elif cnum == 25: return "Road work"
    # elif cnum == 26: return "Traffic signals"
    # elif cnum == 27: return "Pedestrians"
    # elif cnum == 28: return "Children crossing"
    # elif cnum == 29: return "Bicycles crossing"
    # elif cnum == 30: return "Beware of ice/snow"
    # elif cnum == 31: return "Wild animals crossing"
    # elif cnum == 32: return "End of all speed and passing limits"
    elif cnum == 4: return "Turn right ahead"
    elif cnum == 5: return "Turn left ahead"
    # elif cnum == 35: return "Ahead only"
    # elif cnum == 36: return "Go straight or right"
    # elif cnum == 37: return "Go straight or left"
    # elif cnum == 38: return "Keep right"
    # elif cnum == 39: return "Keep left"
    # elif cnum == 40: return "Roundabout mandatory"
    # elif cnum == 41: return "End of no passing"
    # elif cnum == 42: return "End of no passing by vechiles over 3.5 metric tons"
    else: return "Unrecognised Sign"


while True:
    # Capture the frame.
    ret, frame = cap.read()

    # If the frame was not captured, break the loop.
    if not ret:
        break

    # Resize the frame to the input size of the model.
    resized_frame = cv.resize(frame, (150, 150))

    # Convert the frame to RGB.
    resized_frame = cv.cvtColor(resized_frame, cv.COLOR_BGR2RGB)

    # Make a prediction.
    prediction = np.argmax(model.predict(np.array([resized_frame])))
    title = class_label(prediction)

    # Print the prediction.
    print(prediction,title)


    # Display the predicted class on the camera window.
    cv.putText(frame, str(prediction), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv.putText(frame, title, (100, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Display the frame.
    cv.imshow("Frame", frame)

    # Wait for a key press.q
    key = cv.waitKey(1)

    # If the key `q` was pressed, break the loop.
    if key == ord('q'):
        break

# Release the webcam.
cap.release()

# Close all windows.
cv.destroyAllWindows()
