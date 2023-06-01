

from board import boards


from board import boards
import pygame
import math
import copy

from ghost import Ghost


class GameController:
    def __init__(self):
        pygame.init()
        self.level = copy.deepcopy(boards)
        self.num_cells = 22
        self.game = boards
        self.columns = len(level[0])
        self.rows = len(level)
        self.width = self.num_cells * self.columns
        self.height = self.num_cells * self.rows
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.frame_per_second = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(
                f'assets/player_images/{i}.png'), (x_pacman, y_pacman)))
        x_pacman = self.num_cells*1.2
        y_pacman = self.num_cells*1.2
        # blinky
        self.red_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/red.png'), (x_pacman, y_pacman))
        # inky
        self.blue_gh = pygame.transform.scale(pygame.image.load(
            f'assets/ghost_images/blue.png'), (x_pacman, y_pacman))
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
        self.player_x = 15 * self.num_cells  # position init of pacman
        self.player_y = 24 * self.num_cells
        self.direction = 0
        # blinky
        self.red_x = 2*self.num_cells
        self.red_y = 2*self.num_cells
        self.red_direct = 0
        # inky
        self.blue_x = 14*self.num_cells
        self.blue_y = 14*self.num_cells
        self.blue_direct = 2
        # pinky
        self.pink_x = 14*self.num_cells
        self.pink_y = 16*self.num_cells
        self.pink_direct = 2
        # clyde
        self.or_x = 14*self.num_cells
        self.or_y = 16*self.num_cells
        self.targets = [(player_x, player_y), (player_x, player_y),
                        (player_x, player_y), (player_x, player_y)]
    pi = math.pi
    clock = pygame.time.Clock()
    default_color = 'blue'
    player_images = []

    or_direct = 2

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

    def get_targets(self, red_x, red_y, blue_x, blue_y, pink_x, pink_y, or_x, or_y):
        if self.player_x < self.width/2:  # how to avoid player when power up is active
            avoid_x = self.width
        else:
            avoid_x = 0
        if self.player_y < self.height/2:  # how to avoid player when power up is active
            avoid_y = self.height
        else:
            avoid_y = 0
        box = (13*self.num_cells, 15*self.num_cells)  # return to box
        if self.powerup:

            if red.dead:
                red_target = box
            else:
                if eaten_gh[0]:
                    if 11 < red_x//self.num_cells < 19 and 12 < red_y//self.num_cells < 18:
                        red_target = (15*self.num_cells,
                                      self.height*0.1)  # door
                    else:
                        red_target = (player_x, player_y)  # door
                else:
                    red_target = (avoid_x, avoid_y)

            if blue.dead:
                blue_target = box
            else:
                if eaten_gh[1]:
                    if 11 < blue_x//self.num_cells < 19 and 12 < blue_y//self.num_cells < 18:
                        blue_target = (15*self.num_cells,
                                       self.height*0.1)  # door
                    else:
                        blue_target = (player_x, player_y)  # door
                else:
                    blue_target = (player_x, avoid_y)

            if oran.dead:
                or_target = box
            else:
                if eaten_gh[3]:
                    if 11 < or_x//self.num_cells < 19 and 12 < or_y//self.num_cells < 18:
                        or_target = (15*self.num_cells,
                                     self.height*0.1)  # door
                    else:
                        or_target = (player_x, player_y)  # door
                else:
                    or_target = (avoid_x, player_y)

            if pink.dead:
                pink_target = box
            else:
                pink_target = (self.width/2, self.height/3)
        else:
            if not red.dead:
                # box row and col indices 12-18 14-17
                if 11 < red_x//self.num_cells < 19 and 12 < red_y//self.num_cells < 18:
                    red_target = (15*self.num_cells, self.height*0.1)  # door
                else:
                    red_target = (player_x, player_y)
            else:
                red_target = box

            if not blue.dead:
                # print("nor dead")
                if 11 < blue_x//self.num_cells < 19 and 12 < blue_y//self.num_cells < 18:
                    blue_target = (15*self.num_cells, self.height*0.1)
                else:
                    blue_target = (player_x, player_y)
            else:
                blue_target = box

            if not pink.dead:

                if 11 < pink_x//self.num_cells < 19 and 12 < pink_y//self.num_cells < 18:
                    pink_target = (15*self.num_cells, self.height*0.1)
                else:
                    pink_target = (player_x, player_y)
            else:
                pink_target = box

            if not oran.dead:
                if 11 < or_x//self.num_cells < 19 and 12 < or_y//self.num_cells < 18:
                    or_target = (15*self.num_cells, self.height*0.1)
                else:
                    or_target = (player_x, player_y)
            else:
                or_target = box

        return (red_target, blue_target, pink_target, or_target)

    def draw_misc(self):
        score_text = self.font.render(f'Score:{score}', True, 'white')
        self.screen.blit(score_text, (10, self.height-40))
        if powerup:
            pygame.draw.circle(self.screen, 'yellow', (140, self.height-35),
                               15)  # powerup is active
        for i in range(lives):
            self.screen.blit(pygame.transform.scale(
                self.player_images[0], (self.num_cells, self.num_cells)), (self.width-180+i*40, self.height-45))
        if end:
            pygame.draw.rect(self.screen, 'white', [
                             self.width/4-20, self.height/4, self.width/2+25, self.height/2], 0, 10)
            pygame.draw.rect(self.screen, 'black', [
                             self.width/4-5, self.height/4+15, self.width/2, self.height/2-30], 0, 10)
            menu_text = self.font.render(
                'You lost! Press space to restart', True, 'red')
            self.screen.blit(menu_text, (self.width/4, self.height/2))
        if won:
            pygame.draw.rect(self.screen, 'white', [
                             self.width/4-20, self.height/4, self.width/2+25, self.height/2], 0, 10)
            pygame.draw.rect(self.screen, 'black', [
                             self.width/4-5, self.height/4+15, self.width/2, self.heighth/2-30], 0, 10)
            menu_text = self.font.render(
                'You won! Press space to restart', True, 'green')
            self.screen.blit(menu_text, (self.width/4, self.height/2))
        if not begin:
            pygame.draw.rect(self.screen, 'white', [
                             self.width/4-20, self.height/4, self.width/2+25, self.height/2], 0, 10)
            pygame.draw.rect(self.screen, 'black', [
                             self.width/4-5, self.height/4+15, self.width/2, self.height/2-30], 0, 10)
            menu_text = self.font.render('Press space to start', True, 'white')
            self.screen.blit(menu_text, (self.width/4+20, self.height/2))
            # check if we ate dots and update table

    def check_collisions(self, score, powerup, power_count, eaten_gh):

        row = int(center_y//self.num_cells)  # row index of pacman
        col = int(center_x//self.num_cells)  # column index of pacman
        if player_x > 0 and player_x < self.width-self.num_cells:
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

    def draw_board(self):
        for i in range(len(self.level)):  # rows of play board

            for j in range(len(self.level[i])):  # columns of play board
                # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*j,cell*(i+1)),3) #hor
                # pygame.draw.line(screen,'red',(cell*j,cell*i),(cell*(j+1),cell*i),3)#vertical
                if self.level[i][j] == 1:
                    pygame.draw.circle(
                        self.screen, 'white', (j * self.num_cells + 0.5 * self.num_cells, i * self.num_cells + 0.5 * self.num_cells), 4)
                if self.level[i][j] == 2 and not flicker:
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
                self.player_images[counter // 5], (self.player_x, player_y))

        if self.direction == 1:  # left
            self.screen.blit(pygame.transform.flip(
                self.player_images[counter // 5], True, False), (self.player_x, player_y))

        if self.direction == 2:  # up
            self.screen.blit(pygame.transform.rotate(
                self.player_images[counter // 5], 90), (self.player_x, player_y))

        if self.direction == 3:  # down
            self.screen.blit(pygame.transform.rotate(
                self.player_images[counter // 5], 270), (self.player_x, player_y))
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
        for i in range(len(level)):  # rows of play board
            for j in range(len(level[i])):  # columns of play board
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

    def run(self):
        run = True
        while run:
            self.clock.tick(self.frame_per_second)
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
            self.screen.fill('black')
            self.draw_board()

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
                        red_gh, red_direct, red_dead, red_box, 0, level, cell, powerup, w, eaten_gh, screen)
            # inky
            blue = Ghost(blue_x, blue_y, targets[1], ghost_speed[1],
                         blue_gh, blue_direct, blue_dead, blue_box, 1, level, cell, powerup, w, eaten_gh, screen)
            # pinky
            pink = Ghost(pink_x, pink_y, targets[2], ghost_speed[2],
                         pink_gh, pink_direct, pink_dead, pink_box, 2, level, cell, powerup, w, eaten_gh, screen)
            # clide
            oran = Ghost(or_x, or_y, targets[3], ghost_speed[3],
                         or_gh, or_direct, or_dead, or_box, 3, level, cell, powerup, w, eaten_gh, screen)
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

            turns_allowed = self.check_position(center_x, center_y)
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
                player_x, player_y = self.move_player(player_x, player_y)

            # eat dots
            score, powerup, power_count, eaten_gh = self.check_collisions(
                score, powerup, power_count, eaten_gh)

            if powerup and circle.colliderect(red.rect) and not red.dead and eaten_gh[0]:
                if lives > 0:
                    lives -= 1
                    start = 0
                    powerup = False
                    power_counter = 0
                    # position init
                    player_x = 15*self.num_cells  # position init of pacman
                    player_y = 24*self.num_cells
                    direction = 0
                    # blinky
                    red_x = 2*self.num_cells
                    red_y = 2*self.num_cells
                    red_direct = 0
                    # inky
                    blue_x = 14*self.num_cells
                    blue_y = 14*self.num_cells
                    blue_direct = 2
                    # pinky
                    pink_x = 14*self.num_cells
                    pink_y = 16*self.num_cells
                    pink_direct = 2
                    # clyde
                    or_x = 14*self.num_cells
                    or_y = 16*self.num_cells
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
                    player_x = 15*self.num_cells  # position init of pacman
                    player_y = 24*self.num_cells
                    direction = 0
                    # blinky
                    red_x = 2*self.num_cells
                    red_y = 2*self.num_cells
                    red_direct = 0
                    # inky
                    blue_x = 14*self.num_cells
                    blue_y = 14*self.num_cells
                    blue_direct = 2
                    # pinky
                    pink_x = 14*self.num_cells
                    pink_y = 16*self.num_cells
                    pink_direct = 2
                    # clyde
                    or_x = 14*self.num_cells
                    or_y = 16*self.num_cells
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
                    player_x = 15*self.num_cells  # position init of pacman
                    player_y = 24*self.num_cells
                    direction = 0
                    # blinky
                    red_x = 2*self.num_cells
                    red_y = 2*self.num_cells
                    red_direct = 0
                    # inky
                    blue_x = 14*self.num_cells
                    blue_y = 14*self.num_cells
                    blue_direct = 2
                    # pinky
                    pink_x = 14*self.num_cells
                    pink_y = 16*self.num_cells
                    pink_direct = 2
                    # clyde
                    or_x = 14*self.num_cells
                    or_y = 16*self.num_cells
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
                    player_x = 15*self.num_cells  # position init of pacman
                    player_y = 24*self.num_cells
                    direction = 0
                    # blinky
                    red_x = 2*self.num_cells
                    red_y = 2*self.num_cells
                    red_direct = 0
                    # inky
                    blue_x = 14*self.num_cells
                    blue_y = 14*self.num_cells
                    blue_direct = 2
                    # pinky
                    pink_x = 14*self.num_cells
                    pink_y = 16*self.num_cells
                    pink_direct = 2
                    # clyde
                    or_x = 14*self.num_cells
                    or_y = 16*self.num_cells
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
                        player_x = 15*self.num_cells  # position init of pacman
                        player_y = 24*self.num_cells
                        direction = 0
                        # blinky
                        red_x = 2*self.num_cells
                        red_y = 2*self.num_cells
                        red_direct = 0
                        # inky
                        blue_x = 14*self.num_cells
                        blue_y = 14*self.num_cells
                        blue_direct = 2
                        # pinky
                        pink_x = 14*self.num_cells
                        pink_y = 16*self.num_cells
                        pink_direct = 2
                        # clyde
                        or_x = 14*self.num_cells
                        or_y = 16*self.num_cells
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
                        player_x = 15*self.num_cells  # position init of pacman
                        player_y = 24*self.num_cells
                        direction = 0
                        # blinky
                        red_x = 2*self.num_cells
                        red_y = 2*self.num_cells
                        red_direct = 0
                        # inky
                        blue_x = 14*self.num_cells
                        blue_y = 14*self.num_cells
                        blue_direct = 2
                        # pinky
                        pink_x = 14*self.num_cells
                        pink_y = 16*self.num_cells
                        pink_direct = 2
                        # clyde
                        or_x = 14*self.num_cells
                        or_y = 16*self.num_cells
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
