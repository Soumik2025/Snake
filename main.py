import pygame
import random
import tkinter as tk

from tkinter import messagebox
from pygame.math import Vector2
from snake import Food, Snake
from ui import Button
from config import CELL_NUMBER, CELL_SIZE, WIDTH, HEIGHT

pygame.mixer.init()
pygame.init()
game_start = False
run = True

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont("times new roman", 30, False)
clock = pygame.time.Clock()

bite_sound = pygame.mixer.Sound('sound/bite.wav')
game_over_sound = pygame.mixer.Sound('sound/gameover.wav')

food = Food(CELL_SIZE, (255, 0, 0), CELL_NUMBER)
snake = Snake((255, 255, 0), CELL_SIZE)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
mouse_click = False


def check_collision_with_food():
    if food.pos == snake.body[0]:
        snake.new_block = True
        bite_sound.play()
        food.randomize()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:

        root.destroy()
        run = False
        pygame.quit()
    except:
        pass


def check_collision_with_wall():
    if not 0 <= snake.body[0].x < CELL_NUMBER or not 0 <= snake.body[0].y < CELL_NUMBER:
        game_over_sound.play()
        message_box(
            'Game Over', f'You ran into the wall. Score: {len(snake.body)}')

    for block in snake.body[1:]:
        if block == snake.body[0]:
            game_over_sound.play()
            message_box(
                'Game Over', f'You ran into yourself. Score: {len(snake.body)}')


def drawGrid(w, rows, surface):
    x = 0
    y = 0
    for l in range(rows):
        x = x + CELL_SIZE
        y = y + CELL_SIZE

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow():
    pygame.draw.rect(win, (18, 0, 61), (0, 0, WIDTH, HEIGHT))
    drawGrid(WIDTH, CELL_NUMBER, win)
    food.draw(win)
    snake.draw(win)
    pygame.display.update()


def redrawLobby():
    global font
    global mouse_click, game_start
    pygame.draw.rect(win, (18, 0, 61), (0, 0, WIDTH, HEIGHT))
    text = font.render(f"Welcome to Snake", 0, (255, 255, 255))
    win.blit(text, ((WIDTH/2) - 213/2, WIDTH/2))
    btn_text = f"Start Game"
    btn = Button((WIDTH / 2) - 200, 300, 400, 30, btn_text)
    is_over = btn.hover(mouse_pos)
    if is_over:
        if mouse_click:
            game_start = True
    btn.draw(win, is_over)
    pygame.display.update()


while run:
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False

    if game_start:
        clock.tick(60)
        mouse_click = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if snake.direction.y != 1:
                snake.direction = Vector2(0, -1)
        if keys[pygame.K_RIGHT]:
            if snake.direction.x != -1:
                snake.direction = Vector2(1, 0)
        if keys[pygame.K_DOWN]:
            if snake.direction.y != -1:
                snake.direction = Vector2(0, 1)
        if keys[pygame.K_LEFT]:
            if snake.direction.x != 1:
                snake.direction = Vector2(-1, 0)

        redrawWindow()
        check_collision_with_food()
        check_collision_with_wall()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == SCREEN_UPDATE:
                snake.move_snake()
    else:
        redrawLobby()
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

pygame.quit()
