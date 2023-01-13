import pygame
import os
class Battery:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load((os.path.join('Assets', 'battery.png')))
        self.mask = pygame.mask.from_surface(self.image)
        