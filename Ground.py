import pygame

#Mister Ground
class Ground(pygame.sprite.Sprite):

    #TODO - default constructor

    #Constructor
    def __init__(self, left, top, velocity):
        pygame.sprite.Sprite.__init__(self)

        #Instance Variables
        self.velocity = velocity

        #Load the image
        image = pygame.image.load("base.png").convert_alpha()
        self.image = image
        self.rect = self.image.get_rect()

        #Set the position
        self.rect.topleft = (left, top)

    #Update the position of Mister Ground
    #If x or y is not given, assumes moves velocity
    def update(self, left = None, top = None):
        if left == None or top == None:
            self.rect.x += self.velocity
        else:
            self.rect.topleft = (left, top)
                
    #Returns true if the ground is to the left of the display and no longer visible
    def isDead(self):
        return self.rect.right < 0

    #Return the right most position of the rect
    def get_right(self):
        return self.rect.right

    #Return the top of the rect
    def get_top(self):
        return self.rect.top

    #Return the width of the rect
    def get_width(self):
        return self.rect.width
