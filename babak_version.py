

from board import boards


from board import boards
import pygame
import math
import copy
# dynamic posiitioning an d move equation of cell number
pygame.init()
# w=600 #WIDTH
# h=650 #HEIGHT

cell = 22
level = copy.deepcopy(boards)
game = boards

m = len(level[0])  # columns of matrix level
n = len(level)  # rows board nxm
w = cell*m  # WIDTH
h = cell*n+50  # HEIGHT
# board (n x m )Xcell  + 50 pix for score


screen = pygame.display.set_mode([w, h])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
# boards[active_level] 14 min
color = 'blue'  # for 1st level
pi = math.pi


# small mazes
# how to make class out of thw whole game
player_images = []
x_pacman = cell*1.2
y_pacman = cell*1.2
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(
        f'assets/player_images/{i}.png'), (x_pacman, y_pacman)))
# blinky
red_gh = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/red.png'), (x_pacman, y_pacman))
# inky
blue_gh = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/blue.png'), (x_pacman, y_pacman))
# pinky
pink_gh = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/pink.png'), (x_pacman, y_pacman))
# clyde
or_gh = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/orange.png'), (x_pacman, y_pacman))

poweredup = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/powerup.png'), (x_pacman, y_pacman))
dead = pygame.transform.scale(pygame.image.load(
    f'assets/ghost_images/dead.png'), (x_pacman, y_pacman))


# position init
player_x = 15*cell  # position init of pacman
player_y = 24*cell
direction = 0
# blinky
red_x = 2*cell
red_y = 2*cell
red_direct = 0
# inky
blue_x = 14*cell
blue_y = 14*cell
blue_direct = 2
# pinky
pink_x = 14*cell
pink_y = 16*cell
pink_direct = 2
# clyde
or_x = 14*cell
or_y = 16*cell
or_direct = 2

targets = [(player_x, player_y), (player_x, player_y),
           (player_x, player_y), (player_x, player_y)]
red_dead = False
blue_dead = False
or_dead = False
pink_dead = False

red_box = False
blue_box = False
or_box = False
pink_box = False

counter = 0
flicker = False
turns_allowed = [False, False, False, False]  # right left up down
direction_command = 0
player_speed = 2
ghost_speed = [2, 2, 2, 2]
score = 0
powerup = False
power_count = 0
eaten_gh = [False, False, False, False]
moving = False
start = 0
end = False
won = False
lives = 3
begin = False


class Ghost:
    def __init__(self, x, y, target, speed, img, direction, dead, box, id):
        self.x = x
        self.y = y
        self.centerx = self.x+cell//2
        self.centery = self.y+cell//2
        self.target = target
        self.speed = speed
        self.img = img
        self.dead = dead
        self.direction = direction
        self.inbox = box
        self.id = id
        self.turns, self.inbox = self.check_collision()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_gh[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x, self.y))
        elif powerup and not self.dead and not eaten_gh[self.id]:
            screen.blit(poweredup, (self.x, self.y))
        else:
            screen.blit(dead, (self.x, self.y))

        ghos_rect = pygame.rect.Rect(
            (self.centerx-cell//2, self.centery-cell//2), (cell, cell))
        return ghos_rect

    def check_collision(self):
        mid = cell//2
        col = int(self.centerx//cell)
        row = int(self.centery//cell)
        self.turns = [False, False, False, False]
        if 0 < self.centerx//cell < len(level[0])-1:
            # escape the door
            if level[int((self.centery-mid)//cell)][col] == 9:
                self.turns[2] = True

            if level[row][int(self.centerx-mid)//cell] < 3 or (level[row][int(self.centerx-mid)//cell] == 9 and (
                    self.inbox or self.dead)):

                self.turns[1] = True

            if level[row][int(self.centerx+mid)//cell] < 3 or (level[row][int(self.centerx+mid)//cell] == 9 and (
                    self.inbox or self.dead)):

                self.turns[0] = True

            if level[int(self.centery+mid)//cell][col] < 3 or (level[int(self.centery+mid)//cell][col] == 9 and (
                    self.inbox or self.dead)):

                self.turns[3] = True

            if level[int(self.centery-mid)//cell][col] < 3 or (level[int(self.centery-mid)//cell][col] == 9 and (
                    self.inbox or self.dead)):

                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if cell//3 <= self.centerx % cell <= 2*cell//3:
                    if level[int(self.centery+mid)//cell][col] < 3 or (level[int(self.centery+mid)//cell][col] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[3] = True

                    if level[int(self.centery-mid)//cell][col] < 3 or (level[int(self.centery-mid)//cell][col] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[2] = True
                if cell//3 <= self.centery % cell <= 2*cell//3:
                    if level[row][col-1] < 3 or (level[row][col-1] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[1] = True

                    if level[row][col+1] < 3 or (level[row][col+1] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if cell//3 <= self.centerx % cell <= 2*cell//3:
                    if level[int(self.centery+mid)//cell][col] < 3 or (level[int(self.centery+mid)//cell][col] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[3] = True

                    if level[int(self.centery-mid)//cell][col] < 3 or (level[int(self.centery-mid)//cell][col] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[2] = True
                if cell//3 <= self.centery % cell <= 2*cell//3:
                    if level[row][int(self.centerx-mid)//cell] < 3 or (level[row][int(self.centerx-mid)//cell] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[1] = True

                    if level[row][int(self.centerx+mid)//cell] < 3 or (level[row][int(self.centerx+mid)//cell] == 9 and (
                            self.inbox or self.dead)):

                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        if 11 < self.x//cell < 18 and 13 < self.y//cell < 17:
            # box row and col indices 12-18 14-17
            self.inbox = True
        else:
            self.inbox = False

        return self.turns, self.inbox

    def move_or(self):
        # orange turn for pursuit    go right as a rule
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y += self.speed
                else:
                    self.x -= self.speed

        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -5:
            self.x = w-3
        elif self.x > w:
            self.x = - 5
        return self.x, self.y, self.direction

    # blinky behavior
    def move_red(self):
        # red avoid wall and go forward

        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed

        elif self.direction == 1:
            if self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed

        elif self.direction == 2:
            if self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed

                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[2]:
                self.y -= self.speed

        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[3]:
                self.y += self.speed
        if self.x < -5:
            self.x = w-3
        elif self.x > w:
            self.x = - 5
        return self.x, self.y, self.direction

    def move_blue(self):
        # ble turns go up or down to catch pacman , left right to avoid walls
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y += self.speed
                else:
                    self.x -= self.speed

        elif self.direction == 2:
            if self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                self.y -= self.speed

        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                self.y += self.speed
        if self.x < -5:
            self.x = w-3
        elif self.x > w:
            self.x = - 5
        return self.x, self.y, self.direction

    def move_pink(self):  # opposite if blue
        # pink turns left right to catch hero , up down to avoid walls
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed

        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed

                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -5:
            self.x = w-3
        elif self.x > w:
            self.x = - 5
        return self.x, self.y, self.direction


def get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y, or_x, or_y):
    if player_x < w/2:  # how to avoid player when power up is active
        avoid_x = w
    else:
        avoid_x = 0
    if player_y < h/2:  # how to avoid player when power up is active
        avoid_y = h
    else:
        avoid_y = 0
    box = (13*cell, 15*cell)  # return to box
    if powerup:

        if red.dead:
            red_target = box
        else:
            if eaten_gh[0]:
                if 11 < red_x//cell < 19 and 12 < red_y//cell < 18:
                    red_target = (15*cell, h*0.1)  # door
                else:
                    red_target = (player_x, player_y)  # door
            else:
                red_target = (avoid_x, avoid_y)

        if blue.dead:
            blue_target = box
        else:
            if eaten_gh[1]:
                if 11 < blue_x//cell < 19 and 12 < blue_y//cell < 18:
                    blue_target = (15*cell, h*0.1)  # door
                else:
                    blue_target = (player_x, player_y)  # door
            else:
                blue_target = (player_x, avoid_y)

        if oran.dead:
            or_target = box
        else:
            if eaten_gh[3]:
                if 11 < or_x//cell < 19 and 12 < or_y//cell < 18:
                    or_target = (15*cell, h*0.1)  # door
                else:
                    or_target = (player_x, player_y)  # door
            else:
                or_target = (avoid_x, player_y)

        if pink.dead:
            pink_target = box
        else:
            pink_target = (w/2, h/3)
    else:
        if not red.dead:
           # box row and col indices 12-18 14-17
            if 11 < red_x//cell < 19 and 12 < red_y//cell < 18:
                red_target = (15*cell, h*0.1)  # door
            else:
                red_target = (player_x, player_y)
        else:
            red_target = box

        if not blue.dead:
            # print("nor dead")
            if 11 < blue_x//cell < 19 and 12 < blue_y//cell < 18:
                blue_target = (15*cell, h*0.1)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = box

        if not pink.dead:

            if 11 < pink_x//cell < 19 and 12 < pink_y//cell < 18:
                pink_target = (15*cell, h*0.1)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = box

        if not oran.dead:
            if 11 < or_x//cell < 19 and 12 < or_y//cell < 18:
                or_target = (15*cell, h*0.1)
            else:
                or_target = (player_x, player_y)
        else:
            or_target = box

    return (red_target, blue_target, pink_target, or_target)


def draw_misc():
    score_text = font.render(f'Score:{score}', True, 'white')
    screen.blit(score_text, (10, h-40))
    if powerup:
        pygame.draw.circle(screen, 'yellow', (140, h-35),
                           15)  # powerup is active
    for i in range(lives):
        screen.blit(pygame.transform.scale(
            player_images[0], (cell, cell)), (w-180+i*40, h-45))
    if end:
        pygame.draw.rect(screen, 'white', [w/4-20, h/4, w/2+25, h/2], 0, 10)
        pygame.draw.rect(screen, 'black', [w/4-5, h/4+15, w/2, h/2-30], 0, 10)
        menu_text = font.render(
            'You lost! Press space to restart', True, 'red')
        screen.blit(menu_text, (w/4, h/2))
    if won:
        pygame.draw.rect(screen, 'white', [w/4-20, h/4, w/2+25, h/2], 0, 10)
        pygame.draw.rect(screen, 'black', [w/4-5, h/4+15, w/2, h/2-30], 0, 10)
        menu_text = font.render(
            'You won! Press space to restart', True, 'green')
        screen.blit(menu_text, (w/4, h/2))
    if not begin:
        pygame.draw.rect(screen, 'white', [w/4-20, h/4, w/2+25, h/2], 0, 10)
        pygame.draw.rect(screen, 'black', [w/4-5, h/4+15, w/2, h/2-30], 0, 10)
        menu_text = font.render('Press space to start', True, 'white')
        screen.blit(menu_text, (w/4+20, h/2))
        # check if we ate dots and update table


def check_collisions(score, powerup, power_count, eaten_gh):

    row = int(center_y//cell)  # row index of pacman
    col = int(center_x//cell)  # column index of pacman
    if player_x > 0 and player_x < w-cell:
        if level[row][col] == 1:
            level[row][col] = 0
            score += 10
        if level[row][col] == 2:
            level[row][col] = 0
            score += 50
            powerup = True
            power_count = 0
            eaten_gh = [False, False, False, False]

    return score, powerup, power_count, eaten_gh


def draw_board():
    for i in range(len(level)):  # rows of play board

        for j in range(len(level[i])):  # columns of play board
            # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*j,cell*(i+1)),3) #hor
            # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*(j+1),cell*i),3)#vertical
            if level[i][j] == 1:
                pygame.draw.circle(
                    screen, 'white', (j * cell + 0.5 * cell, i * cell + 0.5 * cell), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(
                    screen, 'white', (j * cell + 0.5 * cell, i * cell + 0.5 * cell), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * cell + 0.5 * cell,
                                 i * cell), (j * cell + 0.5 * cell, i * cell + cell), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * cell, i * cell +
                                 0.5 * cell), (j * cell + cell, i * cell + 0.5 * cell), 3)

            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [
                                (j * cell - cell*0.5), i * cell + 0.5*cell, cell, cell], 0, pi/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [
                                (j * cell + cell*0.5), i * cell + 0.5*cell, cell, cell], pi/2, pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [
                                (j * cell + cell*0.5), i * cell - 0.5*cell, cell, cell], pi, 3*pi/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [
                                (j * cell - cell*0.5), i * cell - 0.5*cell, cell, cell], 3*pi/2, pi*2, 3)

            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * cell, i * cell +
                                 0.5 * cell), (j * cell + cell, i * cell + 0.5 * cell), 3)


def draw_player():
    if direction == 0:  # right looking
        screen.blit(player_images[counter // 5], (player_x, player_y))

    if direction == 1:  # left
        screen.blit(pygame.transform.flip(
            player_images[counter // 5], True, False), (player_x, player_y))

    if direction == 2:  # up
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], 90), (player_x, player_y))

    if direction == 3:  # down
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], 270), (player_x, player_y))
    pass


def check_position(x, y):
    turns = [False, False, False, False]
    mid = cell//2  # middle of the cell
    row = int(y//cell)  # row index of pacman
    col = int(x//cell)  # column index of pacman
    # if we could go back and we not in front of wall
    if x // cell < len(level[0])-1:
        if direction == 0:
            if level[row][int(x - mid)//cell] < 3:
                turns[1] = True

        if direction == 1:
            if level[row][int(x + mid)//cell] < 3:
                turns[0] = True

        if direction == 2:
            if level[int(y + mid)//cell][col] < 3:
                turns[3] = True

        if direction == 3:
            if level[int(y - mid)//cell][col] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if cell//3 <= x % cell <= 2*cell//3:  # if we could go up and down
                if level[int(y + mid)//cell][col] < 3:  # position below player
                    turns[3] = True
                if level[int(y - mid)//cell][col] < 3:
                    turns[2] = True
            if cell//3 <= y % cell <= 2*cell//3:
                if level[row][col-1] < 3:
                    turns[1] = True
                if level[row][col+1] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if cell//3 <= x % cell <= 2*cell//3:
                if level[row+1][col] < 3:
                    turns[3] = True
                if level[row-1][col] < 3:
                    turns[2] = True
            if cell//3 <= y % cell <= 2*cell//3:  # if we could go
                if level[row][int(x - mid)//cell] < 3:
                    turns[1] = True
                if level[row][int(x + mid)//cell] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True
    return turns


def draw():
    for i in range(len(level)):  # rows of play board
        for j in range(len(level[i])):  # columns of play board
            score_text = font.render(f'{i}', True, 'white')
            screen.blit(score_text, (cell*j, cell*i))


def draw1():  # box 12-18 14-17
    for k in range(12, 19):
        for j in range(14, 18):
            pygame.draw.circle(screen, 'white', (k * cell, j * cell), 4)


def move_player(x, y):
    # right left up down
    if direction == 0 and turns_allowed[0]:
        x += player_speed
    elif direction == 1 and turns_allowed[1]:
        x -= player_speed
    if direction == 2 and turns_allowed[2]:
        y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        y += player_speed

    return x, y


run = True
while run:
    timer.tick(fps)
    if counter < 19:  # spped of eating my pacman
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    if powerup and power_count < 600:
        power_count += 1
    elif powerup and power_count >= 600:
        power_count = 0
        powerup = False
        eaten_gh = [False, False, False, False]

    if start < 120 and begin:  # and not end and not won:  #second Before start of the game
        moving = False
        start += 1
    else:
        moving = True
    if end or won:
        moving = False
        star = 0
    screen.fill('black')
    draw_board()

    # draw1()
    # ghost
    if powerup:
        ghost_speed = [1, 1.3, 1, 1.2]
        if red_dead:
            ghost_speed[0] = 5
        if blue_dead:
            ghost_speed[1] = 3.5
        if pink_dead:
            ghost_speed[2] = 3.5
        if or_dead:
            ghost_speed[3] = 4

    else:
        ghost_speed = [2, 1.9, 1.8, 1.7]
    if eaten_gh[0]:
        ghost_speed[0] = 2.1
    if eaten_gh[1]:
        ghost_speed[1] = 1.9
    if eaten_gh[2]:
        ghost_speed[2] = 1.8
    if eaten_gh[3]:
        ghost_speed[3] = 1.7
    if red_dead:
        ghost_speed[0] = 5
    if blue_dead:
        ghost_speed[1] = 5
    if pink_dead:
        ghost_speed[2] = 5
    if or_dead:
        ghost_speed[3] = 5

    # blinky
    red = Ghost(red_x, red_y, targets[0], ghost_speed[0],
                red_gh, red_direct, red_dead, red_box, 0)
    # inky
    blue = Ghost(blue_x, blue_y, targets[1], ghost_speed[1],
                 blue_gh, blue_direct, blue_dead, blue_box, 1)
    # pinky
    pink = Ghost(pink_x, pink_y, targets[2], ghost_speed[2],
                 pink_gh, pink_direct, pink_dead, pink_box, 2)
    # clide
    oran = Ghost(or_x, or_y, targets[3], ghost_speed[3],
                 or_gh, or_direct, or_dead, or_box, 3)
    draw_misc()
    # draw()
    targets = get_targets(red_x, red_y, blue_x, blue_y,
                          pink_x, pink_y, or_x, or_y)
    center_x = player_x + cell/2  # +23
    center_y = player_y + cell/2  # +24

    # +2 +1 +1 adapted to picturecould be changed
    if not end and not won and begin:
        draw_player()

    if not end and not won:

        circle = pygame.draw.circle(
            screen, 'black', (center_x+2, center_y+1), cell*1.2/2+1, 2)

    won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            won = False
    if not begin:
        moving = False

    # pygame.draw.circle(screen,'white',(center_x,center_y),2)
# move

    turns_allowed = check_position(center_x, center_y)
    if moving:
        if not red_dead and not red.inbox:
            red_x, red_y, red_direct = red.move_red()
        else:
            red_x, red_y, red_direct = red.move_or()

        if not blue_dead and not blue.inbox:
            blue_x, blue_y, blue_direct = blue.move_blue()
        else:
            blue_x, blue_y, blue_direct = blue.move_or()

        if not pink_dead and not pink.inbox:
            pink_x, pink_y, pink_direct = pink.move_pink()
        else:
            pink_x, pink_y, pink_direct = pink.move_or()

        or_x, or_y, or_direct = oran.move_or()
        player_x, player_y = move_player(player_x, player_y)

    # eat dots
    score, powerup, power_count, eaten_gh = check_collisions(
        score, powerup, power_count, eaten_gh)

    if powerup and circle.colliderect(red.rect) and not red.dead and eaten_gh[0]:
        if lives > 0:
            lives -= 1
            start = 0
            powerup = False
            power_counter = 0
            # position init
            player_x = 15*cell  # position init of pacman
            player_y = 24*cell
            direction = 0
            # blinky
            red_x = 2*cell
            red_y = 2*cell
            red_direct = 0
            # inky
            blue_x = 14*cell
            blue_y = 14*cell
            blue_direct = 2
            # pinky
            pink_x = 14*cell
            pink_y = 16*cell
            pink_direct = 2
            # clyde
            or_x = 14*cell
            or_y = 16*cell
            or_direct = 2
            red_dead = False
            blue_dead = False
            or_dead = False
            pink_dead = False
            eaten_gh = [False, False, False, False]
        else:
            end = True
            moving = False
            start = 0

    if powerup and circle.colliderect(blue.rect) and not blue.dead and eaten_gh[1]:
        if lives > 0:
            lives -= 1
            start = 0
            powerup = False
            power_counter = 0
            # position init
            player_x = 15*cell  # position init of pacman
            player_y = 24*cell
            direction = 0
            # blinky
            red_x = 2*cell
            red_y = 2*cell
            red_direct = 0
            # inky
            blue_x = 14*cell
            blue_y = 14*cell
            blue_direct = 2
            # pinky
            pink_x = 14*cell
            pink_y = 16*cell
            pink_direct = 2
            # clyde
            or_x = 14*cell
            or_y = 16*cell
            or_direct = 2
            eaten_gh = [False, False, False, False]
            red_dead = False
            blue_dead = False
            or_dead = False
            pink_dead = False
        else:
            end = True
            moving = False
            start = 0
    if powerup and circle.colliderect(pink.rect) and not pink.dead and eaten_gh[2]:
        if lives > 0:
            lives -= 1
            start = 0
            powerup = False
            power_counter = 0
            # position init
            player_x = 15*cell  # position init of pacman
            player_y = 24*cell
            direction = 0
            # blinky
            red_x = 2*cell
            red_y = 2*cell
            red_direct = 0
            # inky
            blue_x = 14*cell
            blue_y = 14*cell
            blue_direct = 2
            # pinky
            pink_x = 14*cell
            pink_y = 16*cell
            pink_direct = 2
            # clyde
            or_x = 14*cell
            or_y = 16*cell
            or_direct = 2
            red_dead = False
            blue_dead = False
            or_dead = False
            pink_dead = False
            eaten_gh = [False, False, False, False]
        else:
            end = True
            moving = False
            start = 0
    if powerup and circle.colliderect(oran.rect) and not oran.dead and eaten_gh[3]:
        if lives > 0:
            lives -= 1
            start = 0
            powerup = False
            power_counter = 0
            # position init
            player_x = 15*cell  # position init of pacman
            player_y = 24*cell
            direction = 0
            # blinky
            red_x = 2*cell
            red_y = 2*cell
            red_direct = 0
            # inky
            blue_x = 14*cell
            blue_y = 14*cell
            blue_direct = 2
            # pinky
            pink_x = 14*cell
            pink_y = 16*cell
            pink_direct = 2
            # clyde
            or_x = 14*cell
            or_y = 16*cell
            or_direct = 2
            red_dead = False
            blue_dead = False
            or_dead = False
            pink_dead = False
            eaten_gh = [False, False, False, False]
        else:
            end = True
            moving = False
            start = 0

    if powerup and circle.colliderect(red.rect) and not red.dead and not eaten_gh[0]:
        red_dead = True
        eaten_gh[0] = True
        score += (2 ** eaten_gh.count(True))*100
    if powerup and circle.colliderect(blue.rect) and not blue.dead and not eaten_gh[1]:
        blue_dead = True
        eaten_gh[1] = True
        score += (2 ** eaten_gh.count(True)) * 100
    if powerup and circle.colliderect(pink.rect) and not pink.dead and not eaten_gh[2]:
        pink_dead = True
        eaten_gh[2] = True
        score += (2 ** eaten_gh.count(True))*100

    if powerup and circle.colliderect(oran.rect) and not oran.dead and not eaten_gh[3]:
        or_dead = True
        eaten_gh[3] = True
        score += (2 ** eaten_gh.count(True)) * 100

    if not powerup:
        if (circle.colliderect(red.rect) and not red.dead) or (circle.colliderect(blue.rect) and not blue.dead) or (circle.colliderect(pink.rect) and not pink.dead) or (circle.colliderect(oran.rect) and not oran.dead):
            if lives > 0:
                lives -= 1
                start = 0
                powerup = False
                power_counter = 0
                # position init
                player_x = 15*cell  # position init of pacman
                player_y = 24*cell
                direction = 0
                # blinky
                red_x = 2*cell
                red_y = 2*cell
                red_direct = 0
                # inky
                blue_x = 14*cell
                blue_y = 14*cell
                blue_direct = 2
                # pinky
                pink_x = 14*cell
                pink_y = 16*cell
                pink_direct = 2
                # clyde
                or_x = 14*cell
                or_y = 16*cell
                or_direct = 2
                red_dead = False
                blue_dead = False
                or_dead = False
                pink_dead = False
                eaten_gh = [False, False, False, False]
            else:
                end = True
                moving = False
                start = 0

    if red.inbox and red_dead:
        red_dead = False
    if blue.inbox and blue_dead:
        blue_dead = False
    if pink.inbox and pink_dead:
        pink_dead = False
    if oran.inbox and or_dead:
        or_dead = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not begin:
                begin = True
            if event.key == pygame.K_SPACE and (end or won):

                start = 0
                powerup = False
                power_counter = 0
                # position init
                player_x = 15*cell  # position init of pacman
                player_y = 24*cell
                direction = 0
                # blinky
                red_x = 2*cell
                red_y = 2*cell
                red_direct = 0
                # inky
                blue_x = 14*cell
                blue_y = 14*cell
                blue_direct = 2
                # pinky
                pink_x = 14*cell
                pink_y = 16*cell
                pink_direct = 2
                # clyde
                or_x = 14*cell
                or_y = 16*cell
                or_direct = 2
                red_dead = False
                blue_dead = False
                or_dead = False
                pink_dead = False
                eaten_gh = [False, False, False, False]
                score = 0
                lives = 3

                end = False
                won = False
                # begin=False
                level = copy.deepcopy(boards)
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 0:
                direction_command = direction
    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > w:  # ghost can not move from right to left

        player_x = -5
    elif player_x < -5:
        player_x = w-3
    pygame.display.flip()

pygame.quit()
