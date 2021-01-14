import pygame
from pygame.math import Vector2
import random


class Food(object):
    def __init__(self, side, color, rows):
        self.side = side
        self.color = color
        self.rows = rows
        self.randomize()

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (int(self.pos.x * self.side), int(self.pos.y*self.side), self.side, self.side))

    def randomize(self):
        self.x = random.randint(0, self.rows - 1)
        self.y = random.randint(0, self.rows - 1)
        self.pos = Vector2(self.x, self.y)


class Snake(object):
    def __init__(self, color, size):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.head = self.body[0]
        self.direction = Vector2(1, 0)
        self.color = color
        self.size = size
        self.new_block = False

    def draw(self, win):
        for block in self.body:

            x_pos = int(block.x * self.size)
            y_pos = int(block.y * self.size)
            rect = pygame.Rect(x_pos, y_pos, self.size, self.size)
            pygame.draw.rect(win, self.color, rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]


