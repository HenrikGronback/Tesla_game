import pygame
import os

from car import Car

class Model3(Car):
    def __init__(self, x, y):
        super().__init__(x,y,"model3")