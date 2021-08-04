import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from pyKey import pressKey, releaseKey, press, sendSequence, showKeys

wCam, hCam = 640, 480
frameR = 100
smoothening = 7

pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1, detectionCon=0.75)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1 Find Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2 Get the tip of the index and middle fingers
    if len(lmList)!=0:
        x0, y0 = lmList[4][1:]
        x17, y17 = lmList[17][1:]
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x16, y16 = lmList[16][1:]
        x20, y20 = lmList[20][1:]


        # 3 Check which fingers are up
        fingers = detector.fingersUp()

        # 8 Both Index and middle fingers are up : clicking mode
        lengthQ, img, lineInfo = detector.findDistance(4, 8, img, draw=False, drawC=False)
        lengthW, img, lineInfo = detector.findDistance(4, 12, img, draw=False, drawC=False)
        lengthE, img, lineInfo = detector.findDistance(4, 16, img, draw=False, drawC=False)
        lengthR, img, lineInfo = detector.findDistance(4, 20, img, draw=False, drawC=False)
        lengthD, img, lineInfo = detector.findDistance(8, 12, img, draw=False, drawC=False)
        lengthFlash, img, lineInfo = detector.findDistance(4, 17, img, draw=False, drawC=False)

        if lengthQ < 30:
            cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            press("q")

        if lengthW < 30:
            cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
            press("w")

        if lengthE < 30:
            cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x16, y16), 15, (0, 255, 0), cv2.FILLED)
            press("e")

        if lengthR < 30:
            cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x20, y20), 15, (0, 255, 0), cv2.FILLED)
            press("r")

        if lengthD < 30:
            cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
            press("d")

        if lengthFlash < 30 and y0 > y17:
            cv2.circle(img, (x0, y0), 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x17, y17), 15, (0, 255, 0), cv2.FILLED)
            press("f")


        #     # 9 Finde distance between fingers
        #     length, img, lineInfo = detector.findDistance(8, 12, img, drawC=False)
        #     # print(length)
        #     if length < 40:
        #         cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
        #         cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
        #         # 10 Click mouse if distance short
        #         autopy.mouse.click()
        # if fingers[1]==1 and fingers[2]==1 and fingers[3]==1:
        #     length, img, lineInfo = detector.findDistance(8, 12, img, drawC=False)
        #     length, img, lineInfo = detector.findDistance(12, 16, img, drawC=False)
        #     length, img, lineInfo = detector.findDistance(8, 16, img, draw=False)
        #     # print(length)
        #     if length < 60:
        #         cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
        #         cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
        #         cv2.circle(img, (x16, y16), 15, (0, 255, 0), cv2.FILLED)
        #         # 10 Click mouse if distance short
        #         mouse.right_click()
        
    # 11 Frame Rate
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12 Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)