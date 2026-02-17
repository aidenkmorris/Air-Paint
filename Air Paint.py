import numpy as np
import cv2
from PIL import Image

def get_limits(): 
    lowerLimit = np.array([0, 170, 170], dtype = np.uint8)
    upperLimit = np.array([10, 255, 255], dtype = np.uint8)

    return lowerLimit, upperLimit

colors = {"RED": (0, 0, 255), "ORANGE": (0, 146, 255), "YELLOW": (0, 219, 255), "GREEN": (0, 255, 0), "BLUE":(255, 0, 0), 
          "PURPLE": (255, 0, 188), "WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "BROWN": (0, 42, 97), "PINK": (204, 0, 255)}
color = "RED" #default red
capture = cv2.VideoCapture(0)


prevPoint = None
curPoint = None
buffer = []

while True:
    #read video capture and flip camera
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (1280, 720)) 

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits()

    #color mask and generate box
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        #get coords from box
        x1, y1, x2, y2 = bbox

        #set current point
        curPoint = (int(abs(x2 + x1) / 2), int(abs(y2 + y1) / 2))

        if prevPoint is None:
            prevPoint = curPoint

        #draw previous lines
        for line in buffer:
            cv2.line(frame, line[0], line[1], colors[line[2]], 5)

        #draw current line
        cv2.line(frame, prevPoint, curPoint, colors[color], 5)

        #save current line and current point
        buffer.append([prevPoint, curPoint, color])
        prevPoint = curPoint
    else:
        prevPoint = None
        for line in buffer:
            cv2.line(frame, line[0], line[1], colors[line[2]], 5)

    cv2.imshow("Air Paint", frame)
    cv2.moveWindow("Air Paint", 320, 180)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "): #spacebar saves drawing
        break
    elif key == ord("\b"): #backspace clears screen
        buffer = []
    elif key == ord("1"):
        color = "RED"
    elif key == ord("2"):
        color = "ORANGE"
    elif key == ord("3"):
        color = "YELLOW"
    elif key == ord("4"):
        color = "GREEN"
    elif key == ord("5"):
        color = "BLUE"
    elif key == ord("6"):
        color = "PURPLE"
    elif key == ord("7"):
        color = "PINK"
    elif key == ord("8"):
        color = "WHITE"
    elif key == ord("9"):
        color = "BROWN"
    elif key == ord("0"):
        color = "BLACK"

capture.release() 

cv2.destroyAllWindows()

#gray window
drawing = 150 * np.ones((720, 1280, 3), dtype=np.uint8)

for line in buffer:
            cv2.line(drawing, line[0], line[1], colors[line[2]], 5)

cv2.imshow("Finished Drawing", drawing)
cv2.moveWindow("Finished Drawing", 320, 180)

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "): #spacebar quits
        break

cv2.destroyAllWindows()