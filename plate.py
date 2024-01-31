import pygame

class Plate:
    def __init__(self,x, pygame_surface, player_image):
        self.x = x # Plate's starting x
        self.y = 580 # Plate's y
        self.v = 5 # Plate's starting velocity
        self.hp = 100 # Player's hp starting at 100
        self.score = 0 # Player's score starting from 0
        self.pygame_surface = pygame_surface
        self.player_image = player_image

    def move(self, direction): # moves the cherry according to his current speed and chosen direction
        self.x += self.v * direction

    def show(self): # shows the plate on the screen with his current x and y
        self.pygame_surface.blit(self.player_image, (self.x, self.y))
        # hp color
        color = ()
        if self.hp >= 80:
            color = (0, 255, 0)
        elif self.hp >= 60:
            color = (255, 210, 10)
        elif self.hp >= 40:
            color = (255, 127, 39)
        elif self.hp < 40:
            color = (255, 0, 0)
        # hp border
        pygame.draw.line(self.pygame_surface, (0, 0, 0), (self.x + ((100 - self.hp) / 2), self.y + 70), (self.x + (100 - ((100 - self.hp) / 2)), self.y + 70), 7)
        # hp
        pygame.draw.line(self.pygame_surface, color, (self.x + ((100 - self.hp) / 2), self.y + 70), (self.x + (100 - ((100 - self.hp) / 2)), self.y + 70), 3)

    def Hit(self, cherry):
        return self.x - 50 < cherry.x < self.x + 75 and self.y <= cherry.y + 32 # 52 = the edge of the plate, 20 = the height of the plate