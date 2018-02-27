import pygame
from pygame.locals import *

class TextBox(pygame.sprite.Sprite):
    def __init__(self, bkgrnd, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.initFont()
        self.initImage()
        self.initGroup()
        self.setText(['a','b'])
        self.rect.top = ypos;
        self.rect.left = xpos;
        self.background = bkgrnd
    def initFont(self):
        pygame.font.init()
        self.font = pygame.font.Font(None,3)

    def initImage(self):
        self.image = pygame.Surface((200,80))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
     
    def setText(self,text):
        #tmp = pygame.display.get_surface()
        x_pos = self.rect.left+5
        y_pos = self.rect.top+5

        for t in text:
            x = self.font.render(t,False,(0,0,0))
            self.background.blit(x,(x_pos,y_pos))
            x_pos += 10

            if (x_pos > self.image.get_width()-5):
                x_pos = self.rect.left+5
                y_pos += 10

    def initGroup(self):
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)
