import cv2
# mediapipe is a library to detect hand movements, started at google
import mediapipe as mp #https://google.github.io/mediapipe/solutions/hands
import time


class handDectector():

    def __init__(self, mode = False, max_hands = 2, min_detect_confidence = 0.5, min_track_confidence = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detect_confidence = min_detect_confidence
        self.min_track_confidence = min_track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.min_detect_confidence, self.min_track_confidence)
        # draws lines between points
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # this class only uses RGB so need to convert
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # method called process that processes results
        self.results = self.hands.process(imgRGB)

        # check if multiple hands (max is 2 as defined in the function - see source if needed)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            # hand_landmark represents a single hand
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNum = 0, draw=True):

        lst = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]

            for id, lm in enumerate(myHand.landmark):
                if self.results.multi_hand_landmarks:
                    # print(id, lm)
                    # get the width and height of image
                    h, w, c = img.shape
                    # position of the center, convert to pixels from decimal ratio
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # the id is the id of the landmark on the hand
                    # print(id, cx, cy)
                    lst.append([id, cx, cy])
                    if draw:
                        # example: if you wanted to track a specific location (see below) - id 0 is the first landmark, the base of the hand near the wrist (the carpals)
                        if id == 0:
                            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return lst


def main():
    # used to calculate framerate
    pTime = 0
    # cTime = 0
    cap = cv2.VideoCapture(0)

    #create object
    detector = handDectector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lst = detector.findPosition(img)

        if len(lst) != 0:
            # print(lst[4])
            pass

        # calcuate the framerate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (25, 25), cv2.FONT_ITALIC, 1, (255, 0, 255), 3)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()