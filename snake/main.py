import cv2
from services.snake import SnakeGameClass
from services.handTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.4, maxHands=1)

class snakeGame:
    def start():
        game = SnakeGameClass("bat.png")

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            
            game.showScoreAndLives(img)
            hands, img = detector.findHands(img, flipType=False)

            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == ord('r'):
                game.tries = 3
                game.score = 0
                game.gameOver = False
