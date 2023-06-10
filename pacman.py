

from board import boards
import pygame
import math
import copy
import numpy as np
from ghost3 import Ghost
# 0 = empty black rectangle, 1 = dot, 2 = big dot, 3 = vertical line,
# 4 = horizontal line, 5 = top right, 6 = top left, 7 = bot left, 8 = bot right
# 9 = gate

level_init = [[6, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 5],
              [3, 2, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1,
                  1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3],
              [3, 1, 6, 4, 4, 5, 1, 3, 3, 1, 4, 4, 4, 4,
                  4, 4, 1, 3, 3, 1, 6, 4, 4, 5, 1, 3],
              [3, 1, 3, 6, 4, 8, 1, 7, 8, 1, 4, 4, 4, 4,
                  4, 4, 1, 7, 8, 1, 7, 4, 5, 3, 1, 3],
              [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
              [3, 1, 7, 8, 1, 4, 4, 4, 4, 1, 6, 4, 4, 9,
                  9, 5, 1, 4, 4, 4, 4, 1, 7, 8, 1, 3],
              [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0,
                  0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
              [3, 1, 6, 5, 1, 4, 4, 4, 4, 1, 7, 4, 4, 4,
                  4, 8, 1, 4, 4, 4, 4, 1, 6, 5, 1, 3],
              [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
              [3, 1, 7, 8, 1, 6, 4, 4, 5, 1, 4, 4, 4, 4,
                  4, 4, 1, 6, 4, 4, 5, 1, 7, 8, 1, 3],
              [3, 1, 1, 1, 1, 3, 0, 0, 3, 1, 1, 1, 1, 1,
                  1, 1, 1, 3, 0, 0, 3, 1, 1, 1, 2, 3],
              [7, 4, 4, 4, 4, 8, 0, 0, 7, 4, 4, 4, 4,
                  4, 4, 4, 4, 8, 0, 0, 7, 4, 4, 4, 4, 8]

              ]
level = [
    [6, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 5],
    [3, 2, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1,
     1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 6, 4, 4, 5, 1, 3, 3, 1, 4, 4, 4, 4,
     4, 4, 1, 3, 3, 1, 6, 4, 4, 5, 1, 3],
    [3, 1, 3, 6, 4, 8, 1, 7, 8, 1, 4, 4, 4, 4,
     4, 4, 1, 7, 8, 1, 7, 4, 5, 3, 1, 3],
    [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
    [3, 1, 7, 8, 1, 4, 4, 4, 4, 1, 6, 4, 4, 9,
     9, 5, 1, 4, 4, 4, 4, 1, 7, 8, 1, 3],
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    [3, 1, 6, 5, 1, 4, 4, 4, 4, 1, 7, 4, 4, 4,
     4, 8, 1, 4, 4, 4, 4, 1, 6, 5, 1, 3],
    [3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3],
    [3, 1, 7, 8, 1, 6, 4, 4, 5, 1, 4, 4, 4, 4,
     4, 4, 1, 6, 4, 4, 5, 1, 7, 8, 1, 3],
    [3, 1, 1, 1, 1, 3, 0, 0, 3, 1, 1, 1, 1, 1,
     1, 1, 1, 3, 0, 0, 3, 1, 1, 1, 2, 3],
    [7, 4, 4, 4, 4, 8, 0, 0, 7, 4, 4, 4, 4,
     4, 4, 4, 4, 8, 0, 0, 7, 4, 4, 4, 4, 8]

]


class GameController:
    def __init__(self):
        pygame.init()
        self.level = copy.deepcopy(level)
        self.num_cells = 22
        self.mid_cells = self.num_cells//2
        self.game = boards
        self.columns = len(self.level[0])
        self.rows = len(self.level)
        self.width = self.num_cells * self.columns
        self.height = self.num_cells * self.rows + 50
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.frame_per_second = 120
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        x_pacman = self.num_cells*1.2
        y_pacman = self.num_cells*1.2
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(
                f'assets/player_images/{i}.png'), (x_pacman, y_pacman)))

        # blinky
        self.red_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/red.png'), (x_pacman, y_pacman))
        # inky
        self.blue_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/orange.png'), (x_pacman, y_pacman))
        # pinky
        self.pink_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/pink.png'), (x_pacman, y_pacman))
        # clyde
        self.or_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/orange.png'), (x_pacman, y_pacman))

        self.poweredup = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/powerup.png'), (x_pacman, y_pacman))
        self.dead = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/dead.png'), (x_pacman, y_pacman))

        # position init
        self.player_x = 11 * self.num_cells  # position init of pacman
        self.player_y = 8 * self.num_cells
        self.direction = 0
        # blinky
        self.red_x = 1*self.num_cells * 0.8
        self.red_y = 1*self.num_cells * 0.8
        self.red_direct = 0
        # inky
        self.blue_x = 12*self.num_cells
        self.blue_y = 6*self.num_cells
        self.blue_direct = 2
        self.pink_x = 11*self.num_cells
        self.pink_y = 9*self.num_cells
        self.pink_direct = 2
        self.or_x = 12*self.num_cells
        self.or_y = 6*self.num_cells
        self.or_direct = 2

        self.targets = [(self.player_x, self.player_y), (self.player_x, self.player_y),
                        (self.player_x, self.player_y), (self.player_x, self.player_y)]
        self.red = Ghost(self.red_x, self.red_y, self.targets[0], self.ghost_speed[0],
                         self.red_gh, self.red_direct, self.red_dead, self.red_box, 0, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
        # inky
        self.blue = Ghost(self.or_x, self.or_y, self.targets[1], self.ghost_speed[1],
                          self.or_gh, self.or_direct, self.or_dead, self.or_box, 1, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
        self.draw_misc()

        # draw()
        targets = self.get_targets(self.red_x, self.red_y, self.blue_x,
                                   self.blue_y, self.pink_x, self.pink_y, self.or_x, self.or_y)
    pi = math.pi
    clock = pygame.time.Clock()
    default_color = 'blue'
    player_images = []

    or_direct = 2
    center_y = 0
    center_x = 0
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
    #

    def init_ghosts(self):
        self.red = Ghost(self.red_x, self.red_y, self.targets[0], self.ghost_speed[0],
                         self.red_gh, self.red_direct, self.red_dead, self.red_box, 0, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.dead)
        # inky
        self.blue = Ghost(self.or_x, self.or_y, self.targets[1], self.ghost_speed[1],
                          self.or_gh, self.or_direct, self.or_dead, self.or_box, 1, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)

    def hate_f_gh(self):
        print(self.blue.x//22, self.blue.y//22)

    def get_action_name(self, action):
        match action:
            case 0:
                return "right"
            case 1:
                return "left"
            case 2:
                return "up"
            case 3:
                return "down"
        pass

    def get_states(self):

        walls = np.zeros([int(self.rows), int(self.columns)])  # 1-wall 2-path
        # 1 - dot 2 - powerup
        dots = np.zeros([int(self.rows), int(self.columns)])
        ghosts = np.zeros([int(self.rows), int(self.columns)])
        pacman = np.zeros([int(self.rows), int(self.columns)])

        if self.blue.powerup == True and not self.blue.dead and not self.blue.eaten_ghosts[self.blue.id]:
            ghosts[int((self.blue.y+self.mid_cells)//self.num_cells)][int(
                (self.blue.x+self.mid_cells)//self.num_cells)] = self.blue.direction+1
        else:
            ghosts[int((self.blue.y+self.mid_cells)//self.num_cells)
                   ][int((self.blue.x+self.mid_cells)//self.num_cells)] = -1 * (self.blue.direction+1)

        if self.red.powerup == True and not self.red.dead and not self.red.eaten_ghosts[self.red.id]:
            ghosts[int((self.red.y+self.mid_cells)//self.num_cells)][int(
                (self.red.x+self.mid_cells)//self.num_cells)] = self.red.direction+1
        else:
            ghosts[int((self.red.y+self.mid_cells)//self.num_cells)
                   ][int((self.red.x+self.mid_cells)//self.num_cells)] = -1 * (self.red.direction+1)

        pacman[int((self.player_y+self.mid_cells)//self.num_cells)
               ][int((self.player_x+self.mid_cells)//self.num_cells)] = self.direction + 1

        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 1:
                    dots[i][j] = 1  # means dot
                if self.level[i][j] == 2:
                    dots[i][j] = 2  # means powerup
                if 2 < self.level[i][j] < 10:
                    walls[i][j] = 1  # wall
        x = int((self.player_y+self.mid_cells)//self.num_cells)
        y = int((self.player_x+self.mid_cells)//self.num_cells)
        assert walls[x, y] != 1
        return walls, dots, ghosts, pacman

    def get_targets(self, red_x, red_y, blue_x, blue_y, pink_x, pink_y, or_x, or_y):
        if self.player_x < self.width/2:  # how to avoid player when power up is active
            avoid_x = self.width
        else:
            avoid_x = 0
        if self.player_y < self.height/2:  # how to avoid player when power up is active
            avoid_y = self.height
        else:
            avoid_y = 0
        box = (13*self.num_cells, 6*self.num_cells)  # return to box
        if self.powerup:

            if self.red.dead:
                red_target = box
            else:
                if self.eaten_gh[0]:
                    if 10 < red_x//self.num_cells < 15 and 5 <= red_y//self.num_cells < 7:
                        red_target = (14*self.num_cells,
                                      self.height*0.1)  # door
                    else:
                        red_target = (self.player_x, self.player_y)  # door
                else:
                    red_target = (avoid_x, avoid_y)

            if self.blue.dead:
                blue_target = box
            else:
                if self.eaten_gh[1]:
                    if 10 < blue_x//self.num_cells < 15 and 5 <= blue_y//self.num_cells < 7:
                        blue_target = (14*self.num_cells,
                                       self.height*0.1)  # door
                    else:
                        blue_target = (self.player_x, self.player_y)  # door
                else:
                    blue_target = (self.player_x, avoid_y)

        else:
            if not self.red.dead:
                # box row and col indices 12-18 14-17
                if 10 < red_x//self.num_cells < 15 and 5 <= red_y//self.num_cells < 7:
                    red_target = (14*self.num_cells, self.height*0.1)  # door
                else:
                    red_target = (self.player_x, self.player_y)
            else:
                red_target = box

            if not self.blue.dead:
                # print("nor dead")
                if 10 < blue_x//self.num_cells < 15 and 5 <= blue_y//self.num_cells < 7:
                    blue_target = (14*self.num_cells, self.height*0.1)
                else:
                    blue_target = (self.player_x, self.player_y)
            else:
                blue_target = box

        pink_target = box
        or_target = box

        return (red_target, blue_target, pink_target, or_target)

    def draw_misc(self):
        score_text = self.font.render(f'Score:{self.score}', True, 'white')
        self.screen.blit(score_text, (10, self.height-40))
        if self.powerup:
            pygame.draw.circle(self.screen, 'yellow', (140, self.height-35),
                               15)  # powerup is active
        for i in range(self.lives):
            self.screen.blit(pygame.transform.scale(
                self.player_images[0], (self.num_cells, self.num_cells)), (self.width-180+i*40, self.height-45))
        if self.end:
            pygame.draw.rect(self.screen, 'white', [
                             self.width/4-20, self.height/4, self.width/2+25, self.height/2], 0, 10)
            pygame.draw.rect(self.screen, 'black', [
                             self.width/4-5, self.height/4+15, self.width/2, self.height/2-30], 0, 10)
            menu_text = self.font.render(
                'You lost! Press space to restart', True, 'red')
            self.screen.blit(menu_text, (self.width/4, self.height/2))
        if self.won:
            pygame.draw.rect(self.screen, 'white', [
                             self.width/4-20, self.height/4, self.width/2+25, self.height/2], 0, 10)
            pygame.draw.rect(self.screen, 'black', [
                             self.width/4-5, self.height/4+15, self.width/2, self.height/2-30], 0, 10)
            menu_text = self.font.render(
                'You won! Press space to restart', True, 'green')
            self.screen.blit(menu_text, (self.width/4, self.height/2))

            # check if we ate dots and update table

    def check_collisions(self, score, powerup, power_count, eaten_gh):

        row = int(self.center_y//self.num_cells)  # row index of pacman
        col = int(self.center_x//self.num_cells)  # column index of pacman
        if self.player_x > 0 and self.player_x < self.width-self.num_cells:
            if self.level[row][col] == 1:
                self.level[row][col] = 0
                score += 10
            if self.level[row][col] == 2:
                self.level[row][col] = 0
                score += 50
                powerup = True
                power_count = 0
                eaten_gh = [False, False, False, False]

        return score, powerup, power_count, eaten_gh

    def draw_board(self):
        for i in range(len(self.level)):  # rows of play board

            for j in range(len(self.level[i])):  # columns of play board
                # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*j,cell*(i+1)),3) #hor
                # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*(j+1),cell*i),3)#vertical
                if self.level[i][j] == 1:
                    pygame.draw.circle(
                        self.screen, 'white', (j * self.num_cells + 0.5 * self.num_cells, i * self.num_cells + 0.5 * self.num_cells), 4)
                if self.level[i][j] == 2 and not self.flicker:
                    pygame.draw.circle(
                        self.screen, 'white', (j * self.num_cells + 0.5 * self.num_cells, i * self.num_cells + 0.5 * self.num_cells), 10)
                if self.level[i][j] == 3:
                    pygame.draw.line(self.screen, self.default_color, (j * self.num_cells + 0.5 * self.num_cells,
                                                                       i * self.num_cells), (j * self.num_cells + 0.5 * self.num_cells, i * self.num_cells + self.num_cells), 3)
                if self.level[i][j] == 4:
                    pygame.draw.line(self.screen, self.default_color, (j * self.num_cells, i * self.num_cells +
                                                                       0.5 * self.num_cells), (j * self.num_cells + self.num_cells, i * self.num_cells + 0.5 * self.num_cells), 3)

                if self.level[i][j] == 5:
                    pygame.draw.arc(self.screen, self.default_color, [
                                    (j * self.num_cells - self.num_cells*0.5), i * self.num_cells + 0.5*self.num_cells, self.num_cells, self.num_cells], 0, self.pi/2, 3)
                if self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, self.default_color, [
                                    (j * self.num_cells + self.num_cells*0.5), i * self.num_cells + 0.5*self.num_cells, self.num_cells, self.num_cells], self.pi/2, self.pi, 3)
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, self.default_color, [
                                    (j * self.num_cells + self.num_cells*0.5), i * self.num_cells - 0.5*self.num_cells, self.num_cells, self.num_cells], self.pi, 3*self.pi/2, 3)
                if self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, self.default_color, [
                                    (j * self.num_cells - self.num_cells*0.5), i * self.num_cells - 0.5*self.num_cells, self.num_cells, self.num_cells], 3*self.pi/2, self.pi*2, 3)

                if self.level[i][j] == 9:
                    pygame.draw.line(self.screen, 'white', (j * self.num_cells, i * self.num_cells +
                                                            0.5 * self.num_cells), (j * self.num_cells + self.num_cells, i * self.num_cells + 0.5 * self.num_cells), 3)

    def draw_player(self):
        if self.direction == 0:  # right looking
            self.screen.blit(
                self.player_images[self.counter // 5], (self.player_x, self.player_y))

        if self.direction == 1:  # left
            self.screen.blit(pygame.transform.flip(
                self.player_images[self.counter // 5], True, False), (self.player_x, self.player_y))

        if self.direction == 2:  # up
            self.screen.blit(pygame.transform.rotate(
                self.player_images[self.counter // 5], 90), (self.player_x, self.player_y))

        if self.direction == 3:  # down
            self.screen.blit(pygame.transform.rotate(
                self.player_images[self.counter // 5], 270), (self.player_x, self.player_y))
        pass

    def check_position(self, x, y):
        turns = [False, False, False, False]
        mid = self.num_cells//2  # middle of the self.num_cells
        row = int(y//self.num_cells)  # row index of pacman
        col = int(x//self.num_cells)  # column index of pacman
        # if we could go back and we not in front of wall
        if x // self.num_cells < len(self.level[0])-1:
            if self.direction == 0:
                if self.level[row][int(x - mid)//self.num_cells] < 3:
                    turns[1] = True

            if self.direction == 1:
                if self.level[row][int(x + mid)//self.num_cells] < 3:
                    turns[0] = True

            if self.direction == 2:
                if self.level[int(y + mid)//self.num_cells][col] < 3:
                    turns[3] = True

            if self.direction == 3:
                if self.level[int(y - mid)//self.num_cells][col] < 3:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if self.num_cells//3 <= x % self.num_cells <= 2*self.num_cells//3:  # if we could go up and down
                    # position below player
                    if self.level[int(y + mid)//self.num_cells][col] < 3:
                        turns[3] = True
                    if self.level[int(y - mid)//self.num_cells][col] < 3:
                        turns[2] = True
                if self.num_cells//3 <= y % self.num_cells <= 2*self.num_cells//3:
                    if self.level[row][col-1] < 3:
                        turns[1] = True
                    if self.level[row][col+1] < 3:
                        turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if self.num_cells//3 <= x % self.num_cells <= 2*self.num_cells//3:
                    if self.level[row+1][col] < 3:
                        turns[3] = True
                    if self.level[row-1][col] < 3:
                        turns[2] = True
                if self.num_cells//3 <= y % self.num_cells <= 2*self.num_cells//3:  # if we could go
                    if self.level[row][int(x - mid)//self.num_cells] < 3:
                        turns[1] = True
                    if self.level[row][int(x + mid)//self.num_cells] < 3:
                        turns[0] = True

        else:
            turns[0] = True
            turns[1] = True
        return turns

    def draw(self):
        for i in range(len(self.level)):  # rows of play board
            for j in range(len(self.level[i])):  # columns of play board
                score_text = self.font.render(f'{i}', True, 'white')
                self.screen.blit(
                    score_text, (self.num_cells*j, self.num_cells*i))

    def draw1(self):  # box 12-18 14-17
        for k in range(12, 19):
            for j in range(14, 18):
                pygame.draw.circle(self.screen, 'white',
                                   (k * self.num_cells, j * self.num_cells), 4)

    def move_player(self, x, y):
        # right left up down
        if self.direction == 0 and self.turns_allowed[0]:
            x += self.player_speed
        elif self.direction == 1 and self.turns_allowed[1]:
            x -= self.player_speed
        if self.direction == 2 and self.turns_allowed[2]:
            y -= self.player_speed
        elif self.direction == 3 and self.turns_allowed[3]:
            y += self.player_speed

        return x, y

    def update(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE and (self.end or self.won):

                        self.start = 0
                        self.powerup = False
                        self.power_counter = 0
                        # position init
                        self.player_x = 11*self.num_cells  # position init of pacman
                        self.player_y = 8*self.num_cells
                        self.direction = 0
                        # blinky
                        self.red_x = 1*self.num_cells
                        self.red_y = 1*self.num_cells
                        self.red_direct = 0
                        # inky
                        self.blue_x = 12*self.num_cells
                        self.blue_y = 6*self.num_cells
                        self.blue_direct = 2
                        # pinky
                        self.pink_x = 14*self.num_cells
                        self.pink_y = 16*self.num_cells
                        self.pink_direct = 2
                        # clyde
                        self.or_x = 12*self.num_cells
                        self.or_y = 6*self.num_cells
                        self.or_direct = 2
                        self.red_dead = False
                        self.blue_dead = False
                        self.or_dead = False
                        self.pink_dead = False
                        self.eaten_gh = [False, False, False, False]
                        self.score = 0
                        self.lives = 3
                        self.end = False
                        self.won = False
                        # begin=False
                        self.level = copy.deepcopy(level_init)
                    if event.key == pygame.K_RIGHT:
                        self.direction_command = 0
                    if event.key == pygame.K_LEFT:
                        self.direction_command = 1
                    if event.key == pygame.K_UP:
                        self.direction_command = 2
                    if event.key == pygame.K_DOWN:
                        self.direction_command = 3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and self.direction_command == 0:
                        self.direction_command = self.direction
                    if event.key == pygame.K_LEFT and self.direction_command == 0:
                        self.direction_command = self.direction
                    if event.key == pygame.K_UP and self.direction_command == 0:
                        self.direction_command = self.direction
                    if event.key == pygame.K_DOWN and self.direction_command == 0:
                        self.direction_command = self.direction
            for i in range(4):
                if self.direction_command == i and self.turns_allowed[i]:
                    self.direction = i
            print("direction", self.direction)
            if self.player_x > self.width:  # ghost can not move from right to left

                self.player_x = -5
            elif self.player_x < -5:
                self.player_x = self.width-3
            self.clock.tick(self.frame_per_second)
            if self.counter < 19:  # spped of eating my pacman
                self.counter += 1
                if self.counter > 3:
                    self.flicker = False
            else:
                self.counter = 0
                self.flicker = True

            if self.powerup and self.power_count < 600:
                self.power_count += 1
            elif self.powerup and self.power_count >= 600:
                self.power_count = 0
                self.powerup = False
                self.eaten_gh = [False, False, False, False]

            if self.start < 120:  # and not end and not won:  #second Before start of the game
                self.moving = False
                self.start += 1
            else:
                self.moving = True
            if self.end or self.won:
                self.moving = False
                self.star = 0
            self.screen.fill('black')
            self.draw_board()
            state = self.get_states()

            # draw1()
            # ghost
            # self.hate_f_gh()
            # if self.moving:
            #     print(pacman)

            # print(self.red.powerup)
            if self.powerup:
                self.ghost_speed = [1, 1.3, 1, 1.2]
                if self.red_dead:
                    self.ghost_speed[0] = 5
                if self.blue_dead:
                    self.ghost_speed[1] = 3.5
                if self.pink_dead:
                    self.ghost_speed[2] = 3.5
                if self.or_dead:
                    self.ghost_speed[3] = 4

            else:
                self.ghost_speed = [2, 1.9, 1.8, 1.7]
            if self.eaten_gh[0]:
                self.ghost_speed[0] = 2.1
            if self.eaten_gh[1]:
                self.ghost_speed[1] = 1.9
            if self.eaten_gh[2]:
                self.ghost_speed[2] = 1.8
            if self.eaten_gh[3]:
                self.ghost_speed[3] = 1.7
            if self.red_dead:
                self.ghost_speed[0] = 5
            if self.blue_dead:
                self.ghost_speed[1] = 5
            if self.pink_dead:
                self.ghost_speed[2] = 5
            if self.or_dead:
                self.ghost_speed[3] = 5
            self.red = Ghost(self.red_x, self.red_y, self.targets[0], self.ghost_speed[0],
                             self.red_gh, self.red_direct, self.red_dead, self.red_box, 0, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
            # inky
            self.blue = Ghost(self.blue_x, self.blue_y, self.targets[1], self.ghost_speed[1],
                              self.blue_gh, self.blue_direct, self.blue_dead, self.blue_box, 1, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
            self.draw_misc()
            # draw()
            collided = False
            self.targets = self.get_targets(self.red_x, self.red_y, self.blue_x, self.blue_y,
                                            self.pink_x, self.pink_y, self.or_x, self.or_y)
            self.center_x = self.player_x + self.num_cells/2  # +23
            self.center_y = self.player_y + self.num_cells/2  # +24

            # +2 +1 +1 adapted to picturecould be changed
            if not self.end and not self.won:
                self.draw_player()

            if not self.end and not self.won:

                circle = pygame.draw.circle(
                    self.screen, 'black', (self.center_x+2, self.center_y+1), self.num_cells*1.2/2+1, 2)

            self.won = True
            for i in range(len(self.level)):
                if 1 in self.level[i] or 2 in self.level[i]:
                    self.won = False

            # pygame.draw.circle(screen,'white',(center_x,center_y),2)
        # move

            self.turns_allowed = self.check_position(
                self.center_x, self.center_y)
            if self.moving:
                if not self.red_dead and not self.red.inbox:
                    self.red_x, self.red_y, self.red_direct = self.red.move_red()
                else:
                    self.red_x, self.red_y, self.red_direct = self.red.move_or()

                if not self.blue_dead and not self.blue.inbox:
                    self.blue_x, self.blue_y, self.blue_direct = self.blue.move_or()
                else:
                    self.blue_x, self.blue_y, self.blue_direct = self.blue.move_or()

                self.player_x, self.player_y = self.move_player(
                    self.player_x, self.player_y)

            # eat dots
            self.score, self.powerup, self.power_count, self.eaten_gh = self.check_collisions(
                self.score, self.powerup, self.power_count, self.eaten_gh)

            if self.powerup and circle.colliderect(self.red.rect) and not self.red.dead and self.eaten_gh[0]:
                if self.lives > 0:
                    self.lives -= 1
                    collided = True
                    self.start = 0
                    self.powerup = False
                    self.power_counter = 0
                    # position init
                    self.player_x = 11*self.num_cells  # position init of pacman
                    self.player_y = 8*self.num_cells
                    self.direction = 0
                    # blinky
                    self.red_x = 1*self.num_cells
                    self.red_y = 1*self.num_cells
                    self.red_direct = 0
                    # inky
                    self.blue_x = 12*self.num_cells
                    self.blue_y = 6*self.num_cells
                    self.blue_direct = 2
                    # pinky
                    self.pink_x = 14*self.num_cells
                    self.pink_y = 16*self.num_cells
                    self.pink_direct = 2
                    # clyde
                    self.or_x = 12*self.num_cells
                    self.or_y = 6*self.num_cells
                    self.or_direct = 2
                    self.red_dead = False
                    self.blue_dead = False
                    self.or_dead = False
                    self.pink_dead = False
                    self.eaten_gh = [False, False, False, False]
                else:
                    self.end = True
                    self.moving = False
                    self.start = 0

            if self.powerup and circle.colliderect(self.blue.rect) and not self.blue.dead and self.eaten_gh[1]:
                if self.lives > 0:
                    self.lives -= 1
                    self.start = 0
                    collided = True

                    self.powerup = False
                    self.power_counter = 0
                    # position init
                    self.player_x = 11*self.num_cells  # position init of pacman
                    self.player_y = 8*self.num_cells
                    self.direction = 0
                    # blinky
                    self.red_x = 1*self.num_cells
                    self.red_y = 1*self.num_cells
                    self.red_direct = 0
                    # inky
                    self.blue_x = 12*self.num_cells
                    self.blue_y = 6*self.num_cells
                    self.blue_direct = 2
                    # pinky
                    self.pink_x = 10*self.num_cells
                    self.pink_y = 5*self.num_cells
                    self.pink_direct = 2
                    # clyde
                    self.or_x = 12*self.num_cells
                    self.or_y = 6*self.num_cells
                    self.or_direct = 2
                    self.eaten_gh = [False, False, False, False]
                    self.red_dead = False
                    self.blue_dead = False
                    self.or_dead = False
                    self.pink_dead = False
                else:
                    self.end = True
                    self.moving = False
                    self.start = 0

            if self.powerup and circle.colliderect(self.red.rect) and not self.red.dead and not self.eaten_gh[0]:
                self.red_dead = True
                self.eaten_gh[0] = True
                self.score += (2 ** self.eaten_gh.count(True))*100
            if self.powerup and circle.colliderect(self.blue.rect) and not self.blue.dead and not self.eaten_gh[1]:
                self.blue_dead = True
                self.eaten_gh[1] = True
                self.score += (2 ** self.eaten_gh.count(True)) * 100

            if not self.powerup:
                if (circle.colliderect(self.red.rect) and not self.red.dead) or (circle.colliderect(self.blue.rect) and not self.blue.dead):
                    if self.lives > 0:
                        self.lives -= 1
                        collided = True

                        self.start = 0
                        self.powerup = False
                        self.power_counter = 0
                        # position init
                        self.player_x = 11*self.num_cells  # position init of pacman
                        self.player_y = 8*self.num_cells
                        self.direction = 0
                        # blinky
                        self.red_x = 1*self.num_cells
                        self.red_y = 1*self.num_cells
                        self.red_direct = 0
                        # inky
                        self.blue_x = 12*self.num_cells
                        self.blue_y = 6*self.num_cells
                        self.blue_direct = 2
                        # pinky
                        self.pink_x = 14*self.num_cells
                        self.pink_y = 16*self.num_cells
                        self.pink_direct = 2
                        # clyde
                        self.or_x = 12*self.num_cells
                        self.or_y = 6*self.num_cells
                        self.or_direct = 2
                        self.red_dead = False
                        self.blue_dead = False
                        self.or_dead = False
                        self.pink_dead = False
                        self.eaten_gh = [False, False, False, False]
                    else:
                        self.end = True
                        self.moving = False
                        self.start = 0

            if self.red.inbox and self.red_dead:
                self.red_dead = False
            if self.blue.inbox and self.blue_dead:
                self.blue_dead = False
            if collided:
                print(state)
            pygame.display.flip()
        pygame.quit()
        quit()

    def restart(self):
        self.start = 0
        self.powerup = False
        self.power_counter = 0
        # position init
        self.player_x = 11*self.num_cells  # position init of pacman
        self.player_y = 8*self.num_cells
        self.direction = 0
        # blinky
        self.red_x = 1*self.num_cells
        self.red_y = 1*self.num_cells
        self.red_direct = 0
        # inky
        self.blue_x = 12*self.num_cells
        self.blue_y = 6*self.num_cells
        self.blue_direct = 2
        # pinky
        self.pink_x = 14*self.num_cells
        self.pink_y = 16*self.num_cells
        self.pink_direct = 2
        # clyde
        self.or_x = 12*self.num_cells
        self.or_y = 6*self.num_cells
        self.or_direct = 2
        self.red_dead = False
        self.blue_dead = False
        self.or_dead = False
        self.pink_dead = False
        self.eaten_gh = [False, False, False, False]
        self.score = 0
        self.lives = 3
        self.end = False
        self.won = False
        # begin=False
        self.level = copy.deepcopy(level_init)

    def step(self, action=None):
        if self.end or self.lives == 0:
            self.restart()
        if action != None:
            self.direction_command = action
        for i in range(4):
            if self.direction_command == i and self.turns_allowed[i]:
                self.direction = i

        if self.player_x > self.width:  # ghost can not move from right to left
            self.player_x = -5
        elif self.player_x < -5:
            self.player_x = self.width-3
        self.clock.tick(self.frame_per_second)
        if self.counter < 19:  # spped of eating my pacman
            self.counter += 1
            if self.counter > 3:
                self.flicker = False
        else:
            self.counter = 0
            self.flicker = True
        collided = False
        if self.powerup and self.power_count < 600:
            self.power_count += 1
        elif self.powerup and self.power_count >= 600:
            self.power_count = 0
            self.powerup = False
            self.eaten_gh = [False, False, False, False]

        # if self.start < 120:  # and not end and not won:  #second Before start of the game
        #     self.moving = False
        #     self.start += 1
        # else:
        #     self.moving = True
        self.moving = True
        if self.end or self.won:
            self.moving = False
            self.star = 0
        self.screen.fill('black')
        self.draw_board()

        # draw1()
        # ghost
        # self.hate_f_gh()
        # wall, dot, gh, froz_gh, pacman = self.get_states()
        # if self.moving:
        #     print(pacman)

        # print(self.red.powerup)
        if self.powerup:
            self.ghost_speed = [1, 1.3, 1, 1.2]
            if self.red_dead:
                self.ghost_speed[0] = 5
            if self.blue_dead:
                self.ghost_speed[1] = 3.5
            if self.pink_dead:
                self.ghost_speed[2] = 3.5
            if self.or_dead:
                self.ghost_speed[3] = 4

        else:
            self.ghost_speed = [2, 1.9, 1.8, 1.7]
        if self.eaten_gh[0]:
            self.ghost_speed[0] = 2.1
        if self.eaten_gh[1]:
            self.ghost_speed[1] = 1.9
        if self.eaten_gh[2]:
            self.ghost_speed[2] = 1.8
        if self.eaten_gh[3]:
            self.ghost_speed[3] = 1.7
        if self.red_dead:
            self.ghost_speed[0] = 5
        if self.blue_dead:
            self.ghost_speed[1] = 5
        if self.pink_dead:
            self.ghost_speed[2] = 5
        if self.or_dead:
            self.ghost_speed[3] = 5
        self.red = Ghost(self.red_x, self.red_y, self.targets[0], self.ghost_speed[0],
                         self.red_gh, self.red_direct, self.red_dead, self.red_box, 0, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
        # inky
        self.blue = Ghost(self.blue_x, self.blue_y, self.targets[1], self.ghost_speed[1],
                          self.blue_gh, self.blue_direct, self.blue_dead, self.blue_box, 1, self.level, self.num_cells, self.powerup, self.width, self.eaten_gh, self.screen, self.poweredup, self.dead)
        self.draw_misc()
        # draw()
        self.targets = self.get_targets(self.red_x, self.red_y, self.blue_x, self.blue_y,
                                        self.pink_x, self.pink_y, self.or_x, self.or_y)
        self.center_x = self.player_x + self.num_cells/2  # +23
        self.center_y = self.player_y + self.num_cells/2  # +24

        # +2 +1 +1 adapted to picturecould be changed
        if not self.end and not self.won:
            self.draw_player()

        if not self.end and not self.won:

            circle = pygame.draw.circle(
                self.screen, 'black', (self.center_x+2, self.center_y+1), self.num_cells*1.2/2+1, 2)

        self.won = True
        for i in range(len(self.level)):
            if 1 in self.level[i] or 2 in self.level[i]:
                self.won = False

        # pygame.draw.circle(screen,'white',(center_x,center_y),2)
        # move

        self.turns_allowed = self.check_position(
            self.center_x, self.center_y)
        if self.moving:
            if not self.red_dead and not self.red.inbox:
                self.red_x, self.red_y, self.red_direct = self.red.move_red()
            else:
                self.red_x, self.red_y, self.red_direct = self.red.move_or()

            if not self.blue_dead and not self.blue.inbox:
                self.blue_x, self.blue_y, self.blue_direct = self.blue.move_or()
            else:
                self.blue_x, self.blue_y, self.blue_direct = self.blue.move_or()

            self.player_x, self.player_y = self.move_player(
                self.player_x, self.player_y)

        # eat dots
        self.score, self.powerup, self.power_count, self.eaten_gh = self.check_collisions(
            self.score, self.powerup, self.power_count, self.eaten_gh)
        state = self.get_states()
        if self.powerup and circle.colliderect(self.red.rect) and not self.red.dead and self.eaten_gh[0]:
            if self.lives > 0:
                collided = True
                self.lives -= 1
                self.start = 0
                self.powerup = False
                self.power_counter = 0
                # position init
                self.player_x = 11*self.num_cells  # position init of pacman
                self.player_y = 8*self.num_cells
                self.direction = 0
                # blinky
                self.red_x = 1*self.num_cells
                self.red_y = 1*self.num_cells
                self.red_direct = 0
                # inky
                self.blue_x = 12*self.num_cells
                self.blue_y = 6*self.num_cells
                self.blue_direct = 2
                # pinky
                self.pink_x = 14*self.num_cells
                self.pink_y = 16*self.num_cells
                self.pink_direct = 2
                # clyde
                self.or_x = 12*self.num_cells
                self.or_y = 6*self.num_cells
                self.or_direct = 2
                self.red_dead = False
                self.blue_dead = False
                self.or_dead = False
                self.pink_dead = False
                self.eaten_gh = [False, False, False, False]
            else:
                self.end = True
                self.moving = False
                self.start = 0

        if self.powerup and circle.colliderect(self.blue.rect) and not self.blue.dead and self.eaten_gh[1]:
            if self.lives > 0:
                collided = True
                self.lives -= 1
                self.start = 0
                self.powerup = False
                self.power_counter = 0
                # position init
                self.player_x = 11*self.num_cells  # position init of pacman
                self.player_y = 8*self.num_cells
                self.direction = 0
                # blinky
                self.red_x = 1*self.num_cells
                self.red_y = 1*self.num_cells
                self.red_direct = 0
                # inky
                self.blue_x = 12*self.num_cells
                self.blue_y = 6*self.num_cells
                self.blue_direct = 2
                # pinky
                self.pink_x = 10*self.num_cells
                self.pink_y = 5*self.num_cells
                self.pink_direct = 2
                # clyde
                self.or_x = 12*self.num_cells
                self.or_y = 6*self.num_cells
                self.or_direct = 2
                self.eaten_gh = [False, False, False, False]
                self.red_dead = False
                self.blue_dead = False
                self.or_dead = False
                self.pink_dead = False
            else:
                self.end = True
                self.moving = False
                self.start = 0

        if self.powerup and circle.colliderect(self.red.rect) and not self.red.dead and not self.eaten_gh[0]:
            self.red_dead = True
            self.eaten_gh[0] = True
            self.score += (2 ** self.eaten_gh.count(True))*100
        if self.powerup and circle.colliderect(self.blue.rect) and not self.blue.dead and not self.eaten_gh[1]:
            self.blue_dead = True
            self.eaten_gh[1] = True
            self.score += (2 ** self.eaten_gh.count(True)) * 100

        if not self.powerup:
            if (circle.colliderect(self.red.rect) and not self.red.dead) or (circle.colliderect(self.blue.rect) and not self.blue.dead):
                if self.lives > 0:
                    collided = True
                    self.lives -= 1
                    self.start = 0
                    self.powerup = False
                    self.power_counter = 0
                    # position init
                    self.player_x = 11*self.num_cells  # position init of pacman
                    self.player_y = 8*self.num_cells
                    self.direction = 0
                    # blinky
                    self.red_x = 1*self.num_cells
                    self.red_y = 1*self.num_cells
                    self.red_direct = 0
                    # inky
                    self.blue_x = 12*self.num_cells
                    self.blue_y = 6*self.num_cells
                    self.blue_direct = 2
                    # pinky
                    self.pink_x = 14*self.num_cells
                    self.pink_y = 16*self.num_cells
                    self.pink_direct = 2
                    # clyde
                    self.or_x = 12*self.num_cells
                    self.or_y = 6*self.num_cells
                    self.or_direct = 2
                    self.red_dead = False
                    self.blue_dead = False
                    self.or_dead = False
                    self.pink_dead = False
                    self.eaten_gh = [False, False, False, False]
                else:
                    self.end = True
                    self.moving = False
                    self.start = 0

        if self.red.inbox and self.red_dead:
            self.red_dead = False
        if self.blue.inbox and self.blue_dead:
            self.blue_dead = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.end or self.won):

                    self.start = 0
                    self.powerup = False
                    self.power_counter = 0
                    # position init
                    self.player_x = 11*self.num_cells  # position init of pacman
                    self.player_y = 8*self.num_cells
                    self.direction = 0
                    # blinky
                    self.red_x = 1*self.num_cells
                    self.red_y = 1*self.num_cells
                    self.red_direct = 0
                    # inky
                    self.blue_x = 12*self.num_cells
                    self.blue_y = 6*self.num_cells
                    self.blue_direct = 2
                    # pinky
                    self.pink_x = 14*self.num_cells
                    self.pink_y = 16*self.num_cells
                    self.pink_direct = 2
                    # clyde
                    self.or_x = 12*self.num_cells
                    self.or_y = 6*self.num_cells
                    self.or_direct = 2
                    self.red_dead = False
                    self.blue_dead = False
                    self.or_dead = False
                    self.pink_dead = False
                    self.eaten_gh = [False, False, False, False]
                    self.score = 0
                    self.lives = 3
                    self.end = False
                    self.won = False
                    # begin=False
                    self.level = copy.deepcopy(level_init)
                if event.key == pygame.K_RIGHT:
                    self.direction_command = 0
                if event.key == pygame.K_LEFT:
                    self.direction_command = 1
                if event.key == pygame.K_UP:
                    self.direction_command = 2
                if event.key == pygame.K_DOWN:
                    self.direction_command = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.direction_command == 0:
                    self.direction_command = self.direction
                if event.key == pygame.K_LEFT and self.direction_command == 0:
                    self.direction_command = self.direction
                if event.key == pygame.K_UP and self.direction_command == 0:
                    self.direction_command = self.direction
                if event.key == pygame.K_DOWN and self.direction_command == 0:
                    self.direction_command = self.direction
        if action != None:
            self.direction_command = action
        for i in range(4):
            if self.direction_command == i and self.turns_allowed[i]:
                self.direction = i

        if self.player_x > self.width:  # ghost can not move from right to left
            self.player_x = -5
        elif self.player_x < -5:
            self.player_x = self.width-3
        pygame.display.flip()
        if self.lives == 0:
            self.end = True
        # if action != None and self.turns_allowed[self.direction_command] == False:
        #     print("action", self.get_action_name(action),
        #           self.turns_allowed[self.direction_command])
        return (state, self.score, self.end, self.won, not self.turns_allowed[self.direction_command], collided)


if __name__ == '__main__':
    game = GameController()
    game.update()
