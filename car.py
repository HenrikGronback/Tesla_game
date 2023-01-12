import pygame
import os

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flip = False
        self.stateOfCharge = 1
        self.consumption = 0.005
        self.battery_list = []
        self.gas_list = []
        self.image = pygame.image.load((os.path.join('Assets', 'tesla4real11.png')))
        self.image_flip = pygame.transform.flip(self.image, True, False) #Flip
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_flip = pygame.mask.from_surface(self.image_flip)