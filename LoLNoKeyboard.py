import cv2
import HandTrackingModule as htm
import time
import autopy

####################################################################################
LANDMARK_GROUPS = [(4, 8), (4, 12), (4, 16), (4, 20), (8, 12)]
KEYS = ['q', 'w', 'e', 'r', 'd']
####################################################################################

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

wScr, hScr = autopy.screen.size()
pTime = 0

while True:
    # 1 Find Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    # 2 Get the tip of the index and middle fingers
    if len(lmList)!=0:

        # 3 Check which fingers are up
        fingers = detector.fingersUp()

        # 4 Define touches looking at the distance of the fingers
        img, lengthList = detector.defineTouches(img, LANDMARK_GROUPS)

        # 5 Press Keys (If only the index Up press a specific key)
        img = detector.pressKey(img, lmList, lengthList, KEYS, LANDMARK_GROUPS, (fingers[1]==1 and fingers[2]==0 and fingers[3]==0))

    # 6 Frame Rate
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 7 Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)