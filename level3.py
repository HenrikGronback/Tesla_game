import pygame
import os
import random

from level1 import Level1
from modelS import ModelS
from battery import Battery
from honda import Honda
from gas import Gas

TESLA_HIT_BAT = pygame.USEREVENT + 1
TESLA_HIT_GAS = pygame.USEREVENT + 2
TESLA_NO_JUICE = pygame.USEREVENT + 3
TESLA_HIT_HONDA = pygame.USEREVENT + 4

pygame.font.init()
BATTERY_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
LOSER_FONT = pygame.font.SysFont('comicsans', 60)
font=pygame.font.Font(None,36)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
WIDTH, HEIGHT = 900, 500
X_OFFSET = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 100

class Level3(Level1):
    def __init__(self):
       super().__init__()
       self.car_vel=5
       self.run=True
       self.quit = quit
       self.modelS = ModelS(0,0)
       
        
        

    def level3(self, quit):
        car=ModelS(WIDTH/2-(self.modelS.image.get_width()/2), 170)
        battery=Battery(0,0)
        gas=Gas(0,0)
        honda=Honda(0,0)
        honda_incoming = False
        time_to_honda = 10000
        
        print("level 3")
        
        i = 0

        clock = pygame.time.Clock()
        while self.run:
            clock.tick(FPS)
            text = ""
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
                        text = ""
                        self.draw_window(car, text)
                        self.draw_winner(winner_text)

                if event.type == TESLA_HIT_GAS:
                    loser_text = "You can't charge a Tesla with gas!"
                    text = ""
                    self.draw_window(car, text)
                    self.draw_loser(loser_text)
                    self.restart(quit)
                if event.type == TESLA_NO_JUICE:
                    loser_text = "You ran out of battery!"
                    text = ""
                    self.draw_window(car, text)
                    self.draw_loser(loser_text)
                    self.restart(quit)

                if event.type == TESLA_HIT_HONDA:
                    loser_text = "Oh no, you got Honda bumped!"
                    self.draw_loser(loser_text)
                    self.restart(quit)

            if i % 500 == 0:
                randomNumber = random.randint(0,1)
                if randomNumber == 0:
                    gas = Gas(0, random.randint(20, 500 - gas.image.get_height()))
                    gas.item_vel = random.randint(1,3)
                    car.gas_list_right.append(gas)
                else:
                    gas = Gas(WIDTH, random.randint(20, 500 - gas.image.get_height()))
                    gas.item_vel = random.randint(1,3)
                    car.gas_list_left.append(gas)
                
                

            if i % 200 == 0:
                
                randomNumber = random.randint(0,1)
                if randomNumber == 0:
                    battery = Battery(0,random.randint(20, 500 - battery.image.get_height()))
                    battery.item_vel = random.randint(1,3)
                    car.battery_list_right.append(battery)
                else:
                    battery = Battery(WIDTH,random.randint(20, 500 - battery.image.get_height()))
                    battery.item_vel = random.randint(1,3)
                    car.battery_list_left.append(battery)


            if i % 1000 == 0 and i>0:
                honda_incoming = True
                time_to_honda = 200

            if time_to_honda == 0:
                honda = Honda(-honda.image.get_width(), 300)
                car.honda_list.append(honda)
                honda_incoming = False

            if(honda_incoming):
                time_to_honda -=1
                text = "Beware, Honda bump incoming!"
            else:
                time_to_honda = 10000

            if car.stateOfCharge > 7:
                car.car_vel = car.stateOfCharge
                car.consumption = car.stateOfCharge/1000

            
            keys_pressed = pygame.key.get_pressed()

            self.handle_blue_movement(keys_pressed, car)
            self.check_collision(car)
            self.draw_window(car, text)
            self.handle_object_movement(car, 3)
            
            i = i+1
            
        return quit

    def restart(self, quit):
        WIN.blit(self.background, (0, 20))
        pygame.draw.rect(WIN, (0,0,0), pygame.Rect(0,0,(WIDTH),20))
        
        self.level3(quit)
        

