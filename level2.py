import pygame
import os
import random

from level1 import Level1
from modelY import ModelY
from battery import Battery
from gas import Gas

TESLA_HIT_BAT = pygame.USEREVENT + 1
TESLA_HIT_GAS = pygame.USEREVENT + 2
TESLA_NO_JUICE = pygame.USEREVENT + 3

pygame.font.init()
BATTERY_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
LOSER_FONT = pygame.font.SysFont('comicsans', 60)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
WIDTH, HEIGHT = 900, 500
X_OFFSET = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 100

class Level2(Level1):
    def __init__(self):
       super().__init__()
       self.car_vel=5
       self.run=True
       #self.quit = quit
        
        

    def level2(self, quit):
        car=ModelY(300,300)
        battery=Battery(0,0)
        gas=Gas(0,0)
        print("level 2")
        
        i = 0

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
                        #self.restart()

                if event.type == TESLA_HIT_GAS:
                    loser_text = "You can't charge a Tesla with gas!"
                    self.draw_loser(loser_text)
                    self.restart(quit)
                if event.type == TESLA_NO_JUICE:
                    loser_text = "You ran out of battery!"
                    self.draw_loser(loser_text)
                    self.restart(quit)

            if i % 500 == 0:
                randomNumber = random.randint(0,1)
                if randomNumber == 0:
                    gas = Gas(0, random.randint(20, 500 - gas.image.get_height()))
                    car.gas_list_right.append(gas)
                else:
                    gas = Gas(WIDTH, random.randint(20, 500 - gas.image.get_height()))
                    car.gas_list_left.append(gas)
                
                

            if i % 200 == 0:
                

                randomNumber = random.randint(0,1)
                if randomNumber == 0:
                    battery = Battery(0,random.randint(20, 500 - battery.image.get_height()))
                    car.battery_list_right.append(battery)
                else:
                    battery = Battery(WIDTH,random.randint(20, 500 - battery.image.get_height()))
                    car.battery_list_left.append(battery)
                

            keys_pressed = pygame.key.get_pressed()

            self.handle_blue_movement(keys_pressed, car)

            self.check_collision(car)
            self.draw_window(car)
            self.handle_object_movement(car)
            
            i = i+1
        return quit

    def restart(self, quit):
        WIN.blit(self.background, (0, 20))
        pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))
        
        self.level2(quit)
        

