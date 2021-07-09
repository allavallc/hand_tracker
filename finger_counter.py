import cv2
import os
import time
import hand_tracker_module as htm
import math

# declare variables here
wCam, hCam = 640, 480
###

cap = cv2.VideoCapture(0)
cap.set(3, wCam) # 3 is the width, 4 is the height
cap.set(4, hCam)

#create hand detector
detector = htm.handDectector(min_detect_confidence=0.75)
# create finger tip list
lstFingerTips = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    # create a list of the landmarks
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    #check if there is a hand detected
    # strategy is to get the tips of the fingers and determine if the hand is open or closed
    # https://google.github.io/mediapipe/solutions/hands
    fingerCount = []
    if len(lmList) != 0:
        # [A][B] => B refers to the index, x, and y values, where index is the same as the A valu e
        # for the thumb left hand
        # would need to account for left and right if wanted to check the right hand
        if lmList[lstFingerTips[0]][1] < lmList[lstFingerTips[0]-1][1]:
            fingerCount.append(1)
        else:
            fingerCount.append(0)

        # for the other 4 fingers, regardless of which hand
        for id in range(1, 5):
            if lmList[lstFingerTips[id]][2] < lmList[lstFingerTips[id]-2][2]:
                fingerCount.append(1)
            else:
                fingerCount.append(0)

        # print(fingerCount)
        sumFingers = sum(fingerCount)

        #this puts text
        cv2.putText(img, f'count: {sumFingers}', (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        if sumFingers > 4:
            cv2.putText(img, "position: open", (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        else:
            cv2.putText(img, "position: not open", (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cv2.imshow("Image", img)
    # kill the while loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break