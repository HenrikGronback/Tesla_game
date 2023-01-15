import pygame
import os

class ModelS:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flip = False
        self.stateOfCharge = 1
        self.consumption = 0.007
        self.car_vel = 7
        self.battery_list_right = []
        self.battery_list_left = []
        self.gas_list_right = []
        self.gas_list_left = []
        self.honda_list = []
        self.image = pygame.image.load((os.path.join('Assets', 'modelS.png')))
        self.image_flip = pygame.transform.flip(self.image, True, False) #Flip
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_flip = pygame.mask.from_surface(self.image_flip)