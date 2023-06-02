import random
import time
import cv2
import numpy as np
import pygame
from constants import *
from pacman import GameController
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from PIL import Image

left = pygame.event.Event(pygame.USEREVENT, attr1='left')
right = pygame.event.Event(pygame.USEREVENT, attr1='right')
up = pygame.event.Event(pygame.USEREVENT, attr1='up')
down = pygame.event.Event(pygame.USEREVENT, attr1='down')


class GameWrapper:
    def __init__(self):
        self.controller = GameController()
        self.action = UP

    def start(self):
        self.controller.perform_action(0)

    def restart(self):
        self.controller.restartGame()

    def step(self, action):
        assert action >= 0 and action < 4
        if action == 0:
            event = up
        elif action == 1:
            event = down
        elif action == 2:
            event = left
        elif action == 3:
            event = right
        else:
            print("Invalid action", action)
        pygame.event.post(event)
        data = self.controller.perform_action(action)
        return (data[0], data[1], data[2], data[3])

    def pacman_position(self):
        return self.controller.pacman.position

    def update(self):
        self.controller.update()

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
