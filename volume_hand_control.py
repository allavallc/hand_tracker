import cv2
import numpy as np
import time
import hand_tracker_module as htm
import math
## code from pycaw https://github.com/andremiras/pycaw
# the below libraries worked well on my laptop but not on the RPi
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


##
wCam, hCam = 640, 480
pTime = 0
##

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]
##

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# create the hand object
detector = htm.handDectector()
volBar = 400
volPercentage = 0

while True:
    success, img = cap.read()

    #detect the hands using the detector
    img = detector.findHands(img)
    # get position of hand
    lmList = detector.findPosition(img)
    #check if points exist
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # get the center of the line between the points
        cx, cy = (x1+x2)//2, (y1+y2)//2

        #create circles on the points of the hand
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), 2)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), 2)
        #create a line between the points
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        # the length of the line will correspond to the volume, need the length, using the math function to do that
        length = math.hypot((x2-x1), (y2-y1))
        # print(int(length))

        min = 30
        max = 200
        # hand range was between 0 to about 300
        # need to convert hand range to volume range, use numpy to do this
        vol = np.interp(length, [min, max], [minVol, maxVol])
        #create the volume bar
        volBar = np.interp(length, [min, max], [400, 150])
        # create the volumne percentage
        volPercentage = np.interp(length, [min, max], [0, 100])

        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length <= min:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), 2)
        elif min < length <= max:
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), 2)
        elif length > max:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), 2)
        else:
            print("error 1")

        #create volume bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # dispaly text on screen
    cv2.putText(img, f'{int(fps)}', (35, 35), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(img, f'{int(volPercentage)}%', (75, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv2.imshow("Image", img)

    # kill the while loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break