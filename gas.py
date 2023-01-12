import pygame
import os
class Gas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load((os.path.join('Assets', 'gas4real11.png')))
        self.mask = pygame.mask.from_surface(self.image)