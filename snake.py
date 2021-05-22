"""
-------------------------------------------------------
[program description]
-------------------------------------------------------
Author:  Your Name
ID:      Your ID
Email:   your email@mylaurier.ca
__updated__ = "2021-05-22"
-------------------------------------------------------
"""
import random
import sys

from pygame.math import Vector2
import pygame


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            # rect for positioning
            block_rect = pygame.Rect(
                int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)

            # finding what direction the face is heading
            if index == 0:
                SCREEN.blit(self.head, block_rect)
            # finds the tail
            elif index == len(self.body) - 1:
                SCREEN.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal, block_rect)
                else:
                    # Finds the corners
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        SCREEN.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        SCREEN.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        SCREEN.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        SCREEN.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        self.body.insert(0, self.body[0] + self.direction)
        self.body = self.body[:-1]
        # wrapping borders
        if self.body[0].x < 0:
            self.body[0].x = (CELL_NUMBER - 1)
        if self.body[0].x >= CELL_NUMBER:
            self.body[0].x = 0
        if self.body[0].y < 0:
            self.body[0].y = (CELL_NUMBER - 1)
        if self.body[0].y >= CELL_NUMBER:
            self.body[0].y = 0

    def add_block(self):
        self.body.insert(0, self.body[0] + self.direction)
        self.body = self.body[:]


class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit = pygame.Rect(self.pos.x * CELL_SIZE,
                            self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        SCREEN.blit(apple, fruit)

    def new_fruit(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.game_over()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.new_fruit()
            self.snake.add_block()
            self.score += 1

    def game_over(self):
        if self.snake.body[0] in self.snake.body[1:]:
            print("game over")
            print("Your score was {}".format(self.score))
            pygame.quit()
            sys.exit()

    def draw_grass(self):
        grass_colour = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_colour, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_colour, grass_rect)

    def draw_score(self):
        score_text = FONT.render(
            "Score: {}".format(self.score), True, (0, 0, 255))
        score_rect = pygame.Rect(
            1 * CELL_SIZE, 1 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        SCREEN.blit(score_text, score_rect)


pygame.init()
CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN = pygame.display.set_mode(
    (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
pygame.display.set_caption('Snake')
FONT = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 32)
CLOCK = pygame.time.Clock()
FRAMERATE = 90
apple = pygame.image.load('apple.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
    SCREEN.fill((157, 199, 53))
    main_game.draw_elements()
    pygame.display.update()
    CLOCK.tick(FRAMERATE)
