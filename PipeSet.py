import pygame
from Pipe import Pipe

#Mister Pipe Set
class PipeSet():

    #TODO - Add default constructor

    #Constructor
    def __init__(self, left, gap_center, velocity, color, gap, group):
    #Create the two pipes that make up a pipe set
        self.topPipe = Pipe(left, gap_center - gap / 2, velocity, color, False)
        self.botPipe = Pipe(left, gap_center + gap / 2, velocity, color, True)

        group.add(self.topPipe)
        group.add(self.botPipe)

    #Update the positions of the pipes
    def update(self, left = None, gap_center = None, gap = None):
        #Update the two pipes in the set
        self.topPipe.update(left, gap_center - gap / 2)
        self.botPipe.update(left, gap_center + gap / 2)

    #Returns true if the pipe is to the left of the display and no longer visible
    def isDead(self):
        return self.topPipe.isDead()

    #Returns the left most position of the pipe set
    def get_left(self):
        return self.topPipe.get_left()

    #Returns the right most position of the pipe set
    def get_right(self):
        return self.topPipe.get_right()

    #Set the color of the pipe set
    def set_color(self, color):
        self.topPipe.set_color(color)
        self.botPipe.set_color(color)

    #Returns the top position of the bottom tube
    def get_bottoms_top(self):
        return self.botPipe.get_top()
