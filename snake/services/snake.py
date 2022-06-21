#!/usr/bin/env python
import sys
import math
import random
from cv2 import FONT_HERSHEY_SIMPLEX
from services.helpers import Helpers
import cv2
import json
import numpy as np
from services.handTrackingModule import HandDetector

# VideoCapture(0) for internal webcam
# VideoCapture(1) for external webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Detect hands with handtrac
detector = HandDetector(detectionCon=0.4, maxHands=1)

# Save score
def saveScore(new_data, filename='highscore.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside
        file_data["highscores"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# Define snakeGameClass
class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point
        self.rgb = (0, 0, 0)
        # User has 3 lives/ tries per game
        self.tries = 3
        # Read image Path
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        # First food location
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False
        # Purple snake color
        self.rgb = (109, 67, 126)

    # Shows score and number of lives
    def showScoreAndLives(self, imgMain):
        Helpers.putTextRect(imgMain, f'Score: {self.score}', [50, 80], scale=3, thickness=3, offset=10)
        Helpers.putTextRect(imgMain, f'Lives: {self.tries}', [50, 160], scale=3, thickness=3, offset=10)
        if self.gameOver:
            Helpers.putTextRect(imgMain, f'Game over...', [50, 240], scale=3, thickness=3, offset=10)

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):
        self.showScoreAndLives(imgMain)

        if self.gameOver:
            Helpers.putTextRect(imgMain, "Game Over", [50, 400],
                               scale=2, thickness=5, colorR=(109, 67, 126), font=FONT_HERSHEY_SIMPLEX, offset=20)
            Helpers.putTextRect(imgMain, f'Press "R" for restart, "Q" for exit', [50, 550],
                               scale=2, thickness=5, colorR=(109, 67, 126),font=FONT_HERSHEY_SIMPLEX, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                # self.randomColorHead()
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (109, 67, 126), 20)
                cv2.circle(imgMain, self.points[-1], 20, self.rgb, cv2.FILLED)

            # Draw Food
            imgMain = Helpers.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (238, 194, 255), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                print("Hit")
                self.tries -= 1
                if self.tries < 1:
                    #TO DO WRITE FIREBASE CODE
                    finalScore = { 'username': self.score }
                    saveScore(finalScore)
                    self.gameOver = True
                    self.points = []  # all points of the snake
                    self.lengths = []  # distance between each point
                    self.currentLength = 0  # total length of the snake
                    self.allowedLength = 150  # total allowed Length
                    self.previousHead = 0, 0  # previous head point
                    self.randomFoodLocation()


        return imgMain
