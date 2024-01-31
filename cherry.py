from random import randint
import pygame
class Cherry:
    def __init__(self, n, pygame_surface,cherry_image):
        if n == 1: # Cherry's starting x
            self.x = randint(20,500)
        else:
            self.x = randint(625,1140)
        self.y = 0 # Cherry's starting y
        self.v = 8 # Cherry's starting velocity
        self.pygame_surface = pygame_surface
        self.cherry_image = cherry_image

    def move(self): # moves the cherry according to his current speed
        self.y += self.v

    def show(self): # shows the plate on the screen with his current x and y
        self.pygame_surface.blit(self.cherry_image, (self.x, self.y))