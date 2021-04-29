"""
-------------------------------------------------------
[program description]
-------------------------------------------------------
Author:  Your Name
ID:      Your ID
Email:   your email@mylaurier.ca
__updated__ = "2021-04-29"
-------------------------------------------------------
"""
import pygame
import sys
import random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(
                int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, (43, 216, 17), block_rect)

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
        pygame.draw.rect(SCREEN, (255, 43, 43), fruit)

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
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.new_fruit()
            self.snake.add_block()
            self.score += 1

    def game_over(self):
        if self.snake.body[0] in self.snake.body[1:]:
            print("game over")


pygame.init()
CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN = pygame.display.set_mode(
    (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
CLOCK = pygame.time.Clock()
FRAMERATE = 90

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
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1, 0)
    SCREEN.fill((255, 210, 26))
    main_game.draw_elements()
    pygame.display.update()
    CLOCK.tick(FRAMERATE)
