# Підключаємо потрібні модулі
import random

import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
##################################################################
pygame.init() 

FPS = pygame.time.Clock()
HEIGHT = 800 
WIDTH = 1200

# Підключаємо шрифт
FONT = pygame.font.SysFont('Verdana', 20)

# Сталі змінни для rgb-системи
COLOR_WHITE = (255,255,255) 
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255) 
COLOR_RED = (255, 0, 0) 
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT)) # Задаємо розміри екрана гри

# Додаємо фон
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

# Відкриваємо папку Goose і витаскуємо з неї файли
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


# Аватар гравця 
PLAYER_SIZE = (182, 76) 
player = pygame.image.load("player.png").convert_alpha()
player_rect = pygame.Rect(50, HEIGHT/2, *PLAYER_SIZE)
player_move_down = [0, 4] 
player_move_up = [0, -4] 
player_move_left = [-4, 0]
player_move_right = [4, 0]

# Створення ворогів 
def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy_height = enemy.get_height()
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy_height, HEIGHT - enemy_height), *enemy.get_size()) 
    enemy_move = [random.randint(-8, -4), 0] 
    return [enemy, enemy_rect, enemy_move] 

# Створення бонусів
def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width), - bonus.get_height(), *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move] 


# Івент 1 про ворогами
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500) 
enemies = [] 

# Івент 2, про бонуси
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
bonuses = []

# Івент 3, анімація аватара
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

# Рахунок, початковий номер анімації та запуск гри
score = 0
image_index = 0
playing = True 

# Тіло гри
while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT: 
            playing = False 
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy()) 
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus()) 
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH ,PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # Анімуємо незскінчений задній фон
    bg_X1 -=  bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit((bg), (bg_X1,0))
    main_display.blit((bg), (bg_X2,0))


    # Перевіряємо натискнення клавіш
    keys = pygame.key.get_pressed() 

    # Рух аватара гравця з перевіркою строрін
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    # Створюємо об'єкти і додаємо іх в вікно гри
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    # Виводомо рахунок і аватара
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    
    # Обновлюємо екран
    pygame.display.flip()

    # Видаляємо об'єкти які не на мапі гри
    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))