import cv2
# mediapipe is a library to detect hand movements, started at google
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
# draws lines between points
mpDraw = mp.solutions.drawing_utils

# used to calculate framerate
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    # this class only uses RGB so need to convert
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # method called process that processes results
    results = hands.process(imgRGB)

    # check if multiple hands (max is 2 as defined in the function - see source if needed)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        # hand_landmark represents a single hand
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                print(id, lm)
                # get the width and height of image
                h, w, c = img.shape
                # position of the center, convert to pixels from decimal ratio
                cx, cy = int(lm.x * w), int(lm.y * h)
                # the id is the id of the landmark on the hand
                print(id, cx, cy)

                # example: if you wanted to track a specific location (see below) - id 0 is the first landmark, the base of the hand near the wrist (the carpals)
                # if id == 0:
                #    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

    # calcuate the framerate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (25, 25), cv2.FONT_ITALIC, 1, (255, 0, 255), 3)

    cv2.imshow("Image", img)

    # break the loop if press 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break