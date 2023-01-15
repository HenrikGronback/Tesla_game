import pygame
import random
import os
import math

from model3 import Model3
from battery import Battery
from gas import Gas




TESLA_HIT_BAT = pygame.USEREVENT + 1
TESLA_HIT_GAS = pygame.USEREVENT + 2
TESLA_NO_JUICE = pygame.USEREVENT + 3
TESLA_HIT_HONDA = pygame.USEREVENT + 4

pygame.font.init()
BATTERY_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
LOSER_FONT = pygame.font.SysFont('comicsans', 60)




WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)

ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
WIDTH, HEIGHT = 900, 500
X_OFFSET = 20
FPS = 100
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Level1():
    
    def __init__(self):
        self.background = pygame.transform.scale(ROAD_IMAGE, (WIDTH, HEIGHT))
        self.run = True
        self.model3 = Model3(0,0)


    def level1(self, quit):
        car=Model3(WIDTH/2-(self.model3.image.get_width()/2), 170)
        battery=Battery(0,0)
        gas=Gas(0,0)
        i = 0
        print("level 1")

        clock = pygame.time.Clock()
        while self.run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit = True
                if event.type == TESLA_HIT_BAT:
                    
                    car.stateOfCharge += 1
                    if car.stateOfCharge >= 10:
                        self.run = False
                        self.draw_window(car)
                        winner_text = "Tesla fully charged!"
                        self.draw_winner(winner_text)

                elif event.type == TESLA_HIT_GAS:
                    loser_text = "You can't charge a Tesla with gas!"
                    self.draw_loser(loser_text)
                    self.restart(quit)
                elif event.type == TESLA_NO_JUICE:
                    loser_text = "You ran out of battery!"
                    self.draw_loser(loser_text)
                    self.restart(quit)

            if i % 500 == 0:

                gas = Gas(0, random.randint(20, 500 - gas.image.get_height()))
                car.gas_list_right.append(gas)

            if i % 200 == 0:
                battery = Battery(0,random.randint(20, 500 - battery.image.get_height()))
                car.battery_list_right.append(battery)
                

            keys_pressed = pygame.key.get_pressed()

            self.handle_blue_movement(keys_pressed, car)

            self.check_collision(car)
            self.draw_window(car)
            self.handle_object_movement(car)
            
            i = i+1
        return quit

    def draw_window(self,car, text=""):
        WIN.blit(self.background, (0, 20))
        pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))

        if car.flip:
            WIN.blit(car.image_flip, (car.x, car.y))
        else:
            WIN.blit(car.image, (car.x, car.y))
            
        for bat in car.battery_list_right:
            WIN.blit(bat.image, (bat.x,bat.y))

        for bat in car.battery_list_left:
            WIN.blit(bat.image, (bat.x,bat.y))

        for gas in car.gas_list_right:
            WIN.blit(gas.image, (gas.x, gas.y))

        for gas in car.gas_list_left:
            WIN.blit(gas.image, (gas.x, gas.y))

        for honda in car.honda_list:
            WIN.blit(honda.image_flip, (honda.x, honda.y))
        
        pygame.draw.rect(WIN, (128,128,128), pygame.Rect(0,0,WIDTH,20), 1)
        if car.stateOfCharge < 1:
            pygame.draw.rect(WIN, (255,0,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(WIDTH),20))

        elif car.stateOfCharge >=1 and car.stateOfCharge <= 6:
            pygame.draw.rect(WIN, (255,165,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(WIDTH),20))
        else:
            pygame.draw.rect(WIN, (124,252,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(WIDTH),20))

        draw_text = LOSER_FONT.render(text, True, YELLOW)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        
    
        pygame.display.update()

    def handle_blue_movement(self, keys_pressed, car):
        if keys_pressed[pygame.K_LEFT] and car.x - car.car_vel > 0:  # LEFT
            car.x -= car.car_vel
            car.flip = False
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_RIGHT] and car.x + car.car_vel < WIDTH - int(car.image.get_width()) :  # RIGHT
            car.x += car.car_vel
            car.flip = True
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_UP] and car.y - car.car_vel-X_OFFSET > 0:  # UP
            car.y -= car.car_vel
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_DOWN] and car.y + car.car_vel < HEIGHT - int(car.image.get_height()):  # DOWN
            car.y += car.car_vel
            car.stateOfCharge -=car.consumption
        if car.stateOfCharge <=0:
            pygame.event.post(pygame.event.Event(TESLA_NO_JUICE))

    


    def handle_object_movement(self, car, amplitude = 0):
        
            for bat in car.battery_list_right:
                bat.x += bat.item_vel

            for bat in car.battery_list_left:
                bat.x -= bat.item_vel

            for gas in car.gas_list_right:
                gas.x += gas.item_vel

            for gas in car.gas_list_left:
                gas.x -= gas.item_vel

            for honda in car.honda_list:
                honda.x += honda.car_vel
                angle = 2*math.pi*honda.x/(WIDTH/3)
                sin_value = math.sin(angle) * amplitude
                honda.y += sin_value
                if honda.y > HEIGHT:
                    honda.y = HEIGHT-honda.image.get_height()

    def check_collision(self, car):
        for bat in car.battery_list_right:
            offset_x = car.x - bat.x
            offset_y = car.y - bat.y

            if car.flip:
                collision = bat.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = bat.mask.overlap(car.mask, (int(offset_x), int(offset_y)))
            if collision:
                pygame.event.post(pygame.event.Event(TESLA_HIT_BAT))
                car.battery_list_right.remove(bat)

        for bat in car.battery_list_left:
            offset_x = car.x - bat.x
            offset_y = car.y - bat.y

            if car.flip:
                collision = bat.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = bat.mask.overlap(car.mask, (int(offset_x), int(offset_y)))
            if collision:
                pygame.event.post(pygame.event.Event(TESLA_HIT_BAT))
                car.battery_list_left.remove(bat)

        for gas in car.gas_list_right:
            offset_x = car.x - gas.x
            offset_y = car.y - gas.y

            if car.flip:
                collision = gas.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = gas.mask.overlap(car.mask, ((int(offset_x), int(offset_y))))

            if collision:
                pygame.event.post(pygame.event.Event(TESLA_HIT_GAS))

        for gas in car.gas_list_left:
            offset_x = car.x - gas.x
            offset_y = car.y - gas.y

            if car.flip:
                collision = gas.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = gas.mask.overlap(car.mask, (int(offset_x), int(offset_y)))

            if collision:
                pygame.event.post(pygame.event.Event(TESLA_HIT_GAS))

        for honda in car.honda_list:
            offset_x = car.x - honda.x
            offset_y = car.y - honda.y

            if car.flip:
                collision = honda.mask_flip.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = honda.mask_flip.overlap(car.mask, (int(offset_x), int(offset_y)))

            if collision:
                pygame.event.post(pygame.event.Event(TESLA_HIT_HONDA))



            


    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, True, GREEN)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)


    def draw_loser(self, text):
        draw_text = LOSER_FONT.render(text, True, RED)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)


    def restart(self, quit):
        WIN.blit(self.background, (0, 20))
        pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))
        
        self.level1(quit)

    
