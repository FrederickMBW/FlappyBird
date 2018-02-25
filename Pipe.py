import pygame

#Mister Pipe
class Pipe(pygame.sprite.Sprite):

    #TODO - Add default constructor

    #Returns an image of the pipe when givin a color
    def get_image(self, color):
        return pygame.image.load("pipe-" + color + ".png").convert_alpha()

    #Constructor
    def __init__(self, left, y, velocity, color, isBottom):
        pygame.sprite.Sprite.__init__(self)

        #Instance Variables
        self.velocity = velocity
        self.isBottom = isBottom
        self.color = color

        self.image = self.get_image(color)
        self.rect = self.image.get_rect()

        #Set the position
        if self.isBottom:
            self.rect.topleft = (left, y)
        else:
            self.rect.bottomleft = (left, y)

    #Update the position of Mister Pipe
    #If left or y are not given, assumes moves velocity
    def update(self, left = None, y = None):
        if left == None or y == None:
            self.rect.x += self.velocity
        else:
            if self.isBottom:
                self.rect.topleft = (left, y)
            else:
                self.rect.bottomleft = (left, y)
                
    #Returns true if the pipe is to the left of the display and no longer visible
    def isDead(self):
        return self.rect.right < 0

    #Returns the left most position of the pipe
    def get_left(self):
        return self.rect.left

    #Returns the right most position of the pipe
    def get_right(self):
        return self.rect.right

    #Return the position of the top of the pipe
    def get_top(self):
        return self.rect.top

    #Set the color of the pipe
    def set_color(self, color):
        if self.color != color:
            self.color = color
            self.image = self.get_image(color)
