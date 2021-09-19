import cv2
import HandTrackingModule as htm
import time
import autopy
import cvzone

wCam, hCam = 1280, 720


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img= cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    img = drawAll(img, buttonList)
    cv2.rectangle(img, (1100,0),(1280,60), (255, 255, 0), cv2.FILLED)
    cv2.putText(img, "RESET",  (1120,45) ,
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    if len(lmList) != 0:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            fingers = detector.fingersUp()
            # check 2 fingers up
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                    15, (0, 255, 0), cv2.FILLED)
                    #  select character
                    if (x <= lineInfo[4] <= x+w and y < lineInfo[5] < y+w ):
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        time.sleep(0.2)
                    #  reset finalText
                    if (1100 <= lineInfo[4] <= 1280 and 0 < lineInfo[5] < 60 ):
                        cv2.rectangle(img, (1100,0),(1280,60), (0, 255, 255), cv2.FILLED)
                        cv2.putText(img, "RESET",  (1120,45) ,
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                        finalText = ""
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    cv2.waitKey(1)
    cv2.imshow("Image", img)