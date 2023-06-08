import random
import time
import cv2
import numpy as np
import pygame
from constants import *
from pacman import GameController


class GameWrapper:
    def __init__(self):
        self.controller = GameController()
        self.action = UP
        self.i = 0

    def start(self):
        self.controller.step(0)

    def restart(self):
        self.controller.restart()

    def step(self, action):
        if action != None:
            assert (action >= 0 and action < 4)
        data = self.controller.step(action)
        return (data[0], data[1], data[2], data[3], data[4], data[5])

    def pacman_position(self):
        return self.controller.pacman.position

    def update(self):
        return self.controller.update()

    def process_image(self, obs):
        # image = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
        # image = cv2.resize(image, (210, 160))
        # image = np.array(image, dtype=np.float32) / 255.0
        return obs


if __name__ == "__main__":
    controller = GameController()
    start_time = time.time()

    pygame.time.set_timer(random.choice([up, down, left, right]), 500)

    while True:
        controller.peform_action()
        # current_time = time.time()
        # elapsed_time = current_time - start_time
        # if elapsed_time >= 1:
        #     choice = random.choice([0,1,2,3])
        #     print(choice)
        #     state = controller.peform_action(choice)
        #     current_time = time.time()
        #     start_time = time.time()
