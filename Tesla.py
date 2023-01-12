import pygame
import os
import random

from car import Car
from battery import Battery
from gas import Gas
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
VEL = 3
ITEM_VEL = 1
X_OFFSET = 20


TESLA_HIT_BAT = pygame.USEREVENT + 1
TESLA_HIT_GAS = pygame.USEREVENT + 2
TESLA_NO_JUICE = pygame.USEREVENT + 3


ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
ROAD = pygame.transform.scale(ROAD_IMAGE, (WIDTH, HEIGHT))


def draw_window(car):
    WIN.blit(ROAD, (0, 20))
    pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))
    if car.flip:
        WIN.blit(car.image_flip, (car.x, car.y))
    else:
        WIN.blit(car.image, (car.x, car.y))
        
    for bat in car.battery_list:
        WIN.blit(bat.image, (bat.x,bat.y))

    for gas in car.gas_list:
        WIN.blit(gas.image, (gas.x, gas.y))
    
    pygame.draw.rect(WIN, (124,252,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(WIDTH),20))
    pygame.draw.rect(WIN, (128,128,128), pygame.Rect(0,0,WIDTH,20), 1)
   
    pygame.display.update()


def handle_blue_movement(keys_pressed, car):
    if keys_pressed[pygame.K_LEFT] and car.x - VEL > 0:  # LEFT
        car.x -= VEL
        car.flip = False
        car.stateOfCharge -=car.consumption
    if keys_pressed[pygame.K_RIGHT] and car.x + VEL < WIDTH - int(car.image.get_width()) :  # RIGHT
        car.x += VEL
        car.flip = True
        car.stateOfCharge -=car.consumption
    if keys_pressed[pygame.K_UP] and car.y - VEL-X_OFFSET > 0:  # UP
        car.y -= VEL
        car.stateOfCharge -=car.consumption
    if keys_pressed[pygame.K_DOWN] and car.y + VEL < HEIGHT - int(car.image.get_height()):  # DOWN
        car.y += VEL
        car.stateOfCharge -=car.consumption
    if car.stateOfCharge <=0:
        pygame.event.post(pygame.event.Event(TESLA_NO_JUICE))

    


def handle_object_movement(car):

    for bat in car.battery_list:
        bat.x += ITEM_VEL

    for gas in car.gas_list:
        gas.x += ITEM_VEL

def check_collision(car):
    for bat in car.battery_list:
        offset_x = car.x - bat.x
        offset_y = car.y - bat.y

        if car.flip:
            collision = bat.mask.overlap(car.mask_flip, (offset_x, offset_y))
        else:
            collision = bat.mask.overlap(car.mask, (offset_x, offset_y))
        
        if collision:
            pygame.event.post(pygame.event.Event(TESLA_HIT_BAT))
            car.battery_list.remove(bat)

    for gas in car.gas_list:
        offset_x = car.x - gas.x
        offset_y = car.y - gas.y

        if car.flip:
            collision = gas.mask.overlap(car.mask_flip, (offset_x, offset_y))
        else:
            collision = gas.mask.overlap(car.mask, (offset_x, offset_y))

        if collision:
            pygame.event.post(pygame.event.Event(TESLA_HIT_GAS))
    
    
            


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def draw_loser(text):
    draw_text = LOSER_FONT.render(text, True, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def restart():
    WIN.blit(ROAD, (0, 20))
    pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))
    main()



def main():
    car=Car(300,300)
    battery=Battery(0,0)
    gas=Gas(0,0)
    
    i = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TESLA_HIT_BAT:

                car.stateOfCharge += 1
                if car.stateOfCharge >= 10:
                    draw_window(car)
                    winner_text = "Tesla fully charged!"
                    draw_winner(winner_text)
                    restart()

            if event.type == TESLA_HIT_GAS:
                loser_text = "You can't charge a Tesla with gas!"
                draw_loser(loser_text)
                restart()
            if event.type == TESLA_NO_JUICE:
                loser_text = "You ran out of battery!"
                draw_loser(loser_text)
                restart()

        if i % 500 == 0:

            gas = Gas(0, random.randint(20, 500 - gas.image.get_height()))
            car.gas_list.append(gas)

        if i % 200 == 0:
            battery = Battery(0,random.randint(20, 500 - battery.image.get_height()))
            car.battery_list.append(battery)
            

        keys_pressed = pygame.key.get_pressed()

        handle_blue_movement(keys_pressed, car)

        check_collision(car)
        draw_window(car)
        handle_object_movement(car)
        
        i = i+1

    pygame.quit()


if __name__ == "__main__":
    main()
