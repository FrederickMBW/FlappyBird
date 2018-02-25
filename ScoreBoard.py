import pygame
from pygame.locals import *
# Score Board Class
# Displays Score
class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, background, xpos, ypos):
        super().__init__()
        self.background = background
        self.font = pygame.font.SysFont("comicsansms", 32)
        self.x = xpos
        self.y = ypos
        self.score = 0
    def update(self, score = None):
        if score != None:
            self.score = score

        text = self.font.render(str(self.score), 1, (10, 10, 10))
        textpos = text.get_rect().center = self.x, self.y
        self.background.blit(text, textpos)
