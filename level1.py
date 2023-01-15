import pygame
import random

from model3 import Model3
from battery import Battery
from gas import Gas
from level import Level


class Level1(Level):
    
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(self.ROAD_IMAGE, (self.WIDTH, self.HEIGHT))
        self.run = True
        self.model3 = Model3(0,0)


    def level1(self, quit):
        car=Model3(self.WIDTH/2-(self.model3.image.get_width()/2), 170)
        battery=Battery(0,0)
        gas=Gas(0,0)
        has_died=False
        i = 0

        clock = pygame.time.Clock()
        while self.run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    quit = True
                if event.type == self.TESLA_HIT_BAT:
                    
                    car.stateOfCharge += 1
                    if car.stateOfCharge >= 10:
                        self.run = False
                        self.draw_window(car)
                        winner_text = "Tesla fully charged!"
                        self.draw_winner(winner_text)

                elif event.type == self.TESLA_HIT_GAS:
                    loser_text = "You can't charge a Tesla with gas!"
                    self.draw_loser(loser_text)
                    quit = self.restart(quit, self.level1)

                elif event.type == self.TESLA_NO_JUICE:
                    loser_text = "You ran out of battery!"
                    self.draw_loser(loser_text)
                    quit=self.restart(quit, self.level1)

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

    
