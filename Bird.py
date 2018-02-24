import pygame
import random

#Mister Flappy Bird
class Bird(pygame.sprite.Sprite):
    #Class Variables
    tap_velocity = -10
    acceleration = 1
    max_velocity = 20
    max_angle = -90

    #Used for determining the angle of Mister Flappy Bird
    max_angle_velocity_ratio = max_angle / max_velocity

    #Set all of Mister Flappy Birds values to default at a specific location
    def reset(self, x, y):
        self.velocity = 0
        self.isAlive = True
        self.images = self.getBirdImages()
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #TODO - Constructor with no arguments
    
    #Constructor
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y)
        
    #Get the images for Mister Flappy Bird
    def getBirdImages(self):
        colorCode = ["red", "blue", "yellow"]
        color = random.choice(colorCode)
     
        up = pygame.image.load(color + "bird-upflap.png").convert_alpha()
        mid = pygame.image.load(color + "bird-midflap.png").convert_alpha()
        down = pygame.image.load(color + "bird-downflap.png").convert_alpha()

        return [up, mid, down]

    #Misty Flappy Bird wants to fly!
    def tap(self):
        if self.isAlive:
            self.velocity = self.tap_velocity;

    #Update Mister Flappy Bird's position and angle
    def update(self):
        #Prevent Mister Flappy Bird from going above the top of the screen
        if self.rect.top + self.velocity < 0:
            self.velocity = -self.rect.top

        #If Mister Flappy Bird is at top or above of the screen with a negative velocity, change direction
        if self.rect.top <= 0 and self.velocity <= 0:
            damper = 0.1 #Damper his speed after changing direction
            self.velocity = -self.velocity * damper

        #Prevent Mister Flappy Bird from going too fast downward
        if self.velocity < self.max_velocity:
            self.velocity += self.acceleration

        #Update Mister Flappy Bird's y coordinate
        self.rect.y += self.velocity
        
        #Flap Mister Flappy Bird's wings once after tapping
        #Decide what image of Mister Flappy Bird to use
        if self.velocity < Bird.tap_velocity * 0.75:
            image = self.images[0] 
        elif self.velocity < Bird.tap_velocity * 0.5:
            image = self.images[1]
        elif self.velocity < Bird.tap_velocity * 0.25:
            image = self.images[2]
        elif self.velocity < 0:
            image = self.images[1]
        else:
            image = self.images[0]

        #Calculate Mister Flappy Bird's angle
        angle = Bird.max_angle_velocity_ratio * self.velocity

        #Rotate the image of Mister Flappy Bird
        image = pygame.transform.rotate(image, angle)

        #Update the image and rect of Mister Flappy
        center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
