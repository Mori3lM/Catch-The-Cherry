import pygame

class Button:
    def __init__(self, x, y, height, width, color, on_pos_color, screen, button_text=None, text_color=None, text_size=None):
        self.x = x # button's x
        self.y = y # button's y
        self.height = height # button's height
        self.width = width # button's weight
        self.color = color # button's color
        self.on_pos_color = on_pos_color # button's color pos
        self.screen = screen # screen where to show the button
        self.text_color = text_color # button's text color
        self.button_text = button_text # button's text
        self.text_size = text_size # button's text size

    def is_pressed(self): # checking if the user pressed on the button
        mouse_pos = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]:
            return False
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height

    def draw(self): # shows the button on the screen
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.on_pos_color, (self.x, self.y, self.width, self.height))

        if self.button_text != None:
            font = pygame.font.Font('freesansbold.ttf', self.text_size)
            button_text = font.render(self.button_text, False, self.text_color)
            text_rect = button_text.get_rect()
            text_rect.center = (self.x + self.width // 2), (self.y + self.height // 2)
            self.screen.blit(button_text, text_rect)