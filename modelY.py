import pygame
import os

from car import Car

class ModelY(Car):
    def __init__(self, x, y):
        super().__init__(x,y, "modelY" )
        self.consumption = 0.008
        self.car_vel = 5
        