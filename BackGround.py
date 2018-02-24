import pygame

#Mister Ground
class BackGround(pygame.sprite.Sprite):

    #TODO - add default constructor

    #Constructor
    def __init__(self, left, top, velocity):
        pygame.sprite.Sprite.__init__(self)

        #Instance Variables
        self.velocity = velocity

        #Load the image
        image = pygame.image.load("background-day.png").convert_alpha()
        self.image = image
        self.rect = self.image.get_rect()

        #Set the position
        self.rect.topleft = (left, top)

    #Update the position of Mister Background
    #If x or y is not given, assumes moves velocity
    def update(self, left = None, top = None):
        if left == None or top == None:
            self.rect.x += self.velocity
        else:
            self.rect.topleft = (left, top)
                
    #Returns true if the background is to the left of the display and no longer visible
    def isDead(self):
        return self.rect.right < 0

    #Returns right most position of rect
    def get_right(self):
        return self.rect.right

    #Returns top most position of rect
    def get_top(self):
        return self.rect.top

    #Returns width of rect
    def get_width(self):
        return self.rect.width

    #Sets the image used for the background
    def set_image(self, time):
       self.image = pygame.image.load("background-" + time + ".png").convert_alpha()
