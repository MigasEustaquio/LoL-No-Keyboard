import cv2
import HandTrackingModule as htm
import time
import autopy


wCam, hCam = 640, 480
frameR = 100
smoothening = 7

LANDMARK_GROUPS = [(4, 8), (4, 12), (4, 16), (4, 20), (8, 12)]
KEYS = ['q', 'w', 'e', 'r', 'd']


pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1, detectionCon=0.75)
wScr, hScr = autopy.screen.size()

while True:
    # 1 Find Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2 Get the tip of the index and middle fingers
    if len(lmList)!=0:


        # 3 Check which fingers are up
        fingers = detector.fingersUp()

        img, lengthList = detector.defineButtons(img, LANDMARK_GROUPS)

        if fingers[1]==1 and fingers[2]==0 and fingers[3]==0:
            detector.pressKey(img, lmList, lengthList, KEYS, LANDMARK_GROUPS, False)
        #Para apertar F levanta somente o indicador
        else:
            detector.pressKey(img, lmList, lengthList, KEYS, LANDMARK_GROUPS, True)


    # 11 Frame Rate
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12 Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)