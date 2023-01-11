import pygame
#from pygame.locals import *
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tesla!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

BATTERY_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
LOSER_FONT = pygame.font.SysFont('comicsans', 60)

FPS = 100
TESLA_WIDTH, TESLA_HEIGHT = 395, 127 #592, 191 #1185, 383#395, 127 #448, 176
ACT_TESLA_WIDTH, ACT_TESLA_HEIGHT = 388, 135
VEL = 3
ITEM_VEL = 1
ACT_TESLA_WIDTH_OFFSET = 60
ACT_TESLA_HEIGHT_OFFSET = 25

BAT_WIDTH, bat_HEIGHT = 36, 80

GAS_WIDTH, GAS_HEIGHT = 61, 80


TESLA_HIT_BAT = pygame.USEREVENT + 1
TESLA_HIT_GAS = pygame.USEREVENT + 2

BLUE_TESLA_IMAGE = pygame.image.load((os.path.join('Assets', 'tesla4real11.png')))
BAT_IMAGE = pygame.image.load((os.path.join('Assets', 'batteri.png')))
GAS_CAN_IMAGE = pygame.image.load((os.path.join('Assets', 'gas4real11.png')))
BLUE_TESLA_FLIP = pygame.transform.flip(pygame.transform.scale(BLUE_TESLA_IMAGE, (TESLA_WIDTH, TESLA_HEIGHT)), True, False) #Flip
BLUE_TESLA = (pygame.transform.scale(BLUE_TESLA_IMAGE, (TESLA_WIDTH, TESLA_HEIGHT)))
SUPERCHARGER = (pygame.transform.scale(BAT_IMAGE, (BAT_WIDTH, bat_HEIGHT)))
GAS_CAN = (pygame.transform.scale(GAS_CAN_IMAGE, (GAS_WIDTH, GAS_HEIGHT)))
ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
ROAD = pygame.transform.scale(ROAD_IMAGE, (WIDTH, HEIGHT))

bat_arr = []
gas_arr = []


def draw_window(blue, flip, bat_level):
    WIN.blit(ROAD, (0, 0))
    #bat_level_text = BATTERY_FONT.render("Battery level: " + str(bat_level), 1, BLACK)
    #WIN.blit(bat_level_text, (WIDTH - bat_level_text.get_width() - 10, 10))
    if flip:
        WIN.blit(BLUE_TESLA_FLIP, (blue.x, blue.y))
    else:
        WIN.blit(BLUE_TESLA, (blue.x, blue.y))
    for bat in bat_arr:
        WIN.blit(SUPERCHARGER, (bat.x, bat.y))
    for gas in gas_arr:
        WIN.blit(GAS_CAN, (gas.x, gas.y))
    pygame.draw.rect(WIN, (124,252,0), pygame.Rect(10,10,bat_level*0.1*(WIDTH-20),HEIGHT*0.1))
    pygame.draw.rect(WIN, (128,128,128), pygame.Rect(10,10,WIDTH-20,HEIGHT*0.1), 1)
    pygame.display.update()


def handle_blue_movement(blue, flip, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > 0:  # LEFT
        blue.x -= VEL
        flip = False
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL < WIDTH - TESLA_WIDTH :  # RIGHT
        blue.x += VEL
        flip = True
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL < HEIGHT - TESLA_HEIGHT:  # DOWN
        blue.y += VEL
    return flip


def collision_detection(blue):

    for bat in bat_arr:
        bat.x += ITEM_VEL
        if blue.colliderect(bat):
            bat_arr.remove(bat) 
            pygame.event.post(pygame.event.Event(TESLA_HIT_BAT))
        elif bat.x > WIDTH:
            bat_arr.remove(bat) 

    for gas in gas_arr:
        gas.x += ITEM_VEL
        if blue.colliderect(gas):
            gas_arr.remove(gas)
            pygame.event.post(pygame.event.Event(TESLA_HIT_GAS))
        elif gas.x > WIDTH:
            gas_arr.remove(gas)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_loser(text):
    draw_text = LOSER_FONT.render(text, True, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def restart(flip, blue):
    bat_arr.clear()
    gas_arr.clear()
    bat_level = 0

    WIN.blit(ROAD, (0, 0))
    bat_level_text = BATTERY_FONT.render("Battery level: " + str(bat_level), 1, BLACK)
    WIN.blit(bat_level_text, (WIDTH - bat_level_text.get_width() - 10, 10))
    if flip:
        WIN.blit(BLUE_TESLA_FLIP, (blue.x, blue.y))
    else:
        WIN.blit(BLUE_TESLA, (blue.x, blue.y))

    bat = pygame.Rect(0, random.randint(0, 500 - bat_HEIGHT), BAT_WIDTH, bat_HEIGHT)
    gas = pygame.Rect(10, random.randint(0, 500 - GAS_HEIGHT), GAS_WIDTH, GAS_HEIGHT)
    bat_arr.append(bat)
    gas_arr.append(gas)

    return bat_level


def main():
    bat = pygame.Rect(0, random.randint(0, 500 - bat_HEIGHT), BAT_WIDTH, bat_HEIGHT)
    gas = pygame.Rect(10, random.randint(0, 500 - GAS_HEIGHT), GAS_WIDTH, GAS_HEIGHT)
    blue = pygame.Rect(300, 300, ACT_TESLA_WIDTH, TESLA_HEIGHT)

    i = 0
    bat_arr.append(bat) 
    gas_arr.append(gas)

    clock = pygame.time.Clock()
    run = True
    flip = False
    bat_level = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TESLA_HIT_BAT:

                bat_level += 1
                if bat_level == 10:
                    draw_window(blue, flip, bat_level)
                    winner_text = "Tesla fully charged!"
                    draw_winner(winner_text)
                    bat_level = restart(flip, blue)

            if event.type == TESLA_HIT_GAS:
                loser_text = "You can't charge a Tesla with gas!"
                draw_loser(loser_text)
                bat_level = restart(flip, blue)

        if i % 500 == 0:

            gas = pygame.Rect(0, random.randint(0, 500 - GAS_HEIGHT), GAS_WIDTH, GAS_HEIGHT)
            gas_arr.append(gas)

        if i % 200 == 0:
            bat = pygame.Rect(0, random.randint(0, 500 - bat_HEIGHT), BAT_WIDTH, bat_HEIGHT)
            bat_arr.append(bat)

        keys_pressed = pygame.key.get_pressed()

        flip = handle_blue_movement(blue, flip, keys_pressed)

        draw_window(blue, flip, bat_level)
        collision_detection(blue)
        i = i+1
        print(i)

    pygame.quit()


if __name__ == "__main__":
    main()
