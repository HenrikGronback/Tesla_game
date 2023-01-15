import pygame
import os
from car import Car

class ModelS(Car):
    def __init__(self, x, y):
        super().__init__(x,y,"modelS")
        self.car_vel = 7
        self.consumption = 0.007