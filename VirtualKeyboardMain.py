import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
pTime = 0

detector = HandDetector(detectionCon=0.8)
keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                  ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                  ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()

def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20, rt=0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[80, 80]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100 * x + 25, 100 * k + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = draw(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x-5, y-5), (x + w+5, y + h+5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 45:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN,
                                5, (255, 255, 255), 5)
                    finalText += button.text
                    sleep(0.20)

    cv2.rectangle(img, (50, 350), (700, 450), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (1000, 650), cv2.FONT_HERSHEY_SIMPLEX, 2,
                (0, 0, 0), 3)

    cv2.imshow("ON AIR KEYBOARD", img)
    cv2.waitKey(1)
