#TODOs
#Add exceptions when images are loaded
#Add exceptions for when illegal functions are passed to an object
#Move starting image to a better spot (crop image so bird is centered?)
#Score!
#Button for restarting the game
#The position of the get-ready image could use some improvement!
#Add sounds!
#Ability to exit the game
#Fix the images for the pipe

import pygame
import random
from PipeSet import PipeSet
from Bird import Bird
from Ground import Ground
from BackGround import BackGround
from collections import deque

#Variables
#Screen
screen_width = 288      #Width of the screen 288 is standard
screen_height = 512     #Height of the screen 512 is standard

#Background
background_time = random.choice(["day", "night"])
background_velocity = -1

#Ground
ground_offset = 100           #How far the ground is offset from the bottom of the screen
ground_top = screen_height - ground_offset #The location of the top of the ground

#Pipes
pipe_gap = 100              #The size of the vertical gap between pipes
pipe_spacing = 200          #The spacing from the left of a pipeset to the next pipeset
pipe_gap_variance = 100     #How much the location of the pipeGap is allowed to vary
pipe_count = int(screen_width / pipe_spacing) + 1 #Number of pipes in the pipe deque

#Overall
game_center = ground_top / 2 #The center of the gameplay
game_speed = -5   #The velocity of the pipes and ground

#Bird
bird_start_x = screen_width / 3          #The starting x position for the center of the bird
bird_start_y = game_center        #The starting y position for the center of the bird

#Random Images
main_message_x = screen_width / 2
main_message_y = game_center / 2

tap_image = pygame.image.load("tap.png")
tap_image_rect = tap_image.get_rect()
tap_image_rect.center = (screen_width / 2, game_center)
start_image = pygame.image.load("start.png")
start_image_rect = start_image.get_rect()
start_image_rect.center = (main_message_x, main_message_y)
gameover_image = pygame.image.load("gameover.png")
gameover_image_rect = gameover_image.get_rect()
gameover_image_rect.center = (main_message_x, main_message_y)
getready_image = pygame.image.load("getready.png")
getready_image_rect = getready_image.get_rect()
getready_image_rect.center = (main_message_x, main_message_y)

#Create sprite groups
bird_sprites = pygame.sprite.Group()
ground_sprites = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#Screen
game_display = pygame.display.set_mode((screen_width,screen_height))  #Create the display for the game

#Pipes
#Function for calculating center of gap
def get_pipe_gap():
    return game_center + random.randint(-pipe_gap_variance, pipe_gap_variance)

#Resets the pipe to their default position
def reset_pipes():
    for i in range(len(pipes)):
        left = screen_width + pipe_spacing * i
        gap_center = get_pipe_gap()
        pipes[i].update(left, gap_center, pipe_gap)
        
        #Make the last pipe red
        if i == pipe_count - 1:
            color = "red"
        else:
            color = "green"

        pipes[i].set_color(color)

#Create a deque to hold all the pipes
#Use defalt values for the pipes created
pipes = deque()
for i in range(pipe_count):        
    pipe_set = PipeSet(0, 0, game_speed, "red", pipe_gap, pipe_sprites)
    pipes.append(pipe_set)

#Position all the pipes
reset_pipes()

#Bird
bird = Bird(bird_start_x, bird_start_y)     #Create the bird
bird_sprites.add(bird)                      #Add the bird to the bird sprites group

#Returns a deque of sprites at a given height that spans the screen
#Add the sprites to the givin group
#Assumes the starting position is the left of the screen
def horizontalTile(cls, y, velocity, group):
    item = cls(0, y, velocity)
    item_width = item.get_width()
    item_count = int(screen_width / item_width) + 2 
    items = deque()
    for i in range(item_count):
        item = cls(i * item_width, y, velocity)        
        items.append(item)
        group.add(item)

    return items

#Create the ground sprites
grounds = horizontalTile(Ground, ground_top, game_speed, ground_sprites)

#Create the background sprites
backgrounds = horizontalTile(BackGround, 0, background_velocity, background_sprites)
for background in backgrounds:
    background.set_image(background_time)

#Draw all the sprites in the correct order
def draw_all_sprites():
    background_sprites.draw(game_display)
    pipe_sprites.draw(game_display)
    bird_sprites.draw(game_display)
    ground_sprites.draw(game_display)

#Add all the sprites to a single group
all_sprites.add(background_sprites, pipe_sprites, bird_sprites, ground_sprites)

#Turn on the display
pygame.display.flip()

#Clock
clock = pygame.time.Clock()

#Moves a pipe that is off the left of the screen to after the farthest right pipe
def move_pipes():
    if pipes[0].isDead():
        left = pipes[-1].get_left() + pipe_spacing
        temp = pipes.popleft()
        gap_center = get_pipe_gap()
        temp.update(left, gap_center, pipe_gap)
        pipes.append(temp)

#Moves a sprite that is off the left of the screen to after the farthest right sprite
#This only works when the velocity is a negative for the deque!
def deque_update(deque):
    if deque[0].isDead():
        left = deque[-1].get_right()
        top = deque[-1].get_top()
        temp = deque.popleft()
        temp.update(left, top)
        deque.append(temp)

#Play the game
def dead_screen():
    dead = True
    while dead:
        #Bird falls until it hits the ground
        if not pygame.sprite.spritecollide(bird, ground_sprites, False):
            bird_sprites.update()

        #Exit the dead screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                dead = False

        #Update the display
        draw_all_sprites()
        game_display.blit(gameover_image, gameover_image_rect)
        pygame.display.update()
        clock.tick(40)

def active_game():
    active = True
    while active:

        #Make Mister Flappy Bird Fly if any button is tapped or mouse button clicked
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                bird.tap()

        #Update the sprites and display
        all_sprites.update()
        move_pipes()
        deque_update(grounds)
        deque_update(backgrounds)
        draw_all_sprites()
        pygame.display.update()
        clock.tick(40)

        #If bird collides with the ground or a pipe, exit active game
        if pygame.sprite.spritecollide(bird, pipe_sprites, False) or pygame.sprite.spritecollide(bird, ground_sprites, False):
            bird.velocity = 0
            active = False

def intro_screen():    
    intro = True
    while intro:
        #Exit intro screen if any button is tapped or mouse button hit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                bird.tap()
                intro = False

        #Update the pertinent sprites and display
        background_sprites.update()
        ground_sprites.update()
        deque_update(grounds)
        deque_update(backgrounds)
        draw_all_sprites()
        game_display.blit(tap_image, tap_image_rect)
        game_display.blit(getready_image, getready_image_rect)
        pygame.display.update()
        clock.tick(40)

def reset():
    bird.reset(bird_start_x, bird_start_y)
    reset_pipes()
    all_sprites.draw(game_display)
    pygame.display.update()

running = True
while running:
    intro_screen()
    active_game()
    dead_screen()
    reset()
