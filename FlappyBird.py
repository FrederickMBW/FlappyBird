#TODOs
#Add exceptions when images are loaded
#Add exceptions for when illegal functions are passed to an object
#Encapsulation of objects
#Add sounds!
#Add the ability to exit the game?
#Make the red pipes appear randomly?
#Increase the difficulty of the game based on score?
#Moving Pipes?
#Have the bird move up and down at the get_ready screen?
#Update collision detection? Only do collison detection for the current pipe set? Detection for ground based on birds height?

autoPlay = True

import pygame
import random
import math
from PipeSet import PipeSet
from Bird import Bird
from Ground import Ground
from BackGround import BackGround
from ScoreBoard import ScoreBoard
from collections import deque
from Button import Button

# initialize pygame mixer
pygame.mixer.init()

# load sound for collision
# must be a wav file
# effect = pygame.mixer.Sound("sound_effects.wav")

# load music for background
pygame.mixer.music.load("theme.ogg")

# play background music, -1 is for repeating
pygame.mixer.music.play(-1)

#Variables
#Game States
#Make Enumerated
welcome_state = 0
get_ready_state = 1
play_state = 2
dead_state = 3

#Screen
screen_width = 1000      #Width of the screen 288 is standard
screen_height = 512     #Height of the screen 512 is standard

#Background
background_time = random.choice(["day", "night"])
background_velocity = -1

#Ground
ground_offset = 100           #How far the ground is offset from the bottom of the screen
ground_top = screen_height - ground_offset #The location of the top of the ground

#Pipes
pipe_gap = 100              #The size of the vertical gap between pipes #100 works well!
pipe_spacing =300          #The spacing from the left of a pipeset to the next pipeset #200 works well!
pipe_gap_variance = 100     #How much the location of the pipeGap is allowed to vary
pipe_count = int(screen_width / pipe_spacing) + 1 #Number of pipes in the pipe deque
pipe_count = max(pipe_count, 2) #There must be atleast two pipes for the scoreing system to work

#Overall
game_center = ground_top / 2 #The center of the gameplay
center_line = screen_width / 2 #horizontal center of the display
game_speed = -5   #The velocity of the pipes and ground

#Bird
bird_start_x = screen_width / 3          #The starting x position for the center of the bird
bird_start_y = game_center        #The starting y position for the center of the bird

#Scoreboard
pygame.font.init()
scoreboard_x = center_line
scoreboard_y = game_center / 6

#Load Random Images
main_message_x = center_line
main_message_y = game_center / 2

tap_image = pygame.image.load("tap.png")
tap_image_rect = tap_image.get_rect()
tap_image_rect.center = (center_line, game_center)
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
start_button_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#Screen
game_display = pygame.display.set_mode((screen_width,screen_height))  #Create the display for the game

#Scoreboard
scoreboard = ScoreBoard(game_display, scoreboard_x, scoreboard_y)

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

#Start Button
button_y = game_center
start_button = Button(center_line, button_y)
start_button_sprite.add(start_button)

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

#Add all the sprites to a single group
all_sprites.add(background_sprites, pipe_sprites, bird_sprites, ground_sprites)

#Draw all the sprites in the correct order
def draw_all_sprites():
    background_sprites.draw(game_display)
    pipe_sprites.draw(game_display)
    bird_sprites.draw(game_display)
    ground_sprites.draw(game_display)

#Turn on the display
pygame.display.flip()

#Clock
clock = pygame.time.Clock()
tick_rate = 40

#Moves a pipe that is off the left of the screen to after the farthest right pipe
def move_pipes():
    if pipes[0].isDead():
        left = pipes[-1].get_left() + pipe_spacing
        temp = pipes.popleft()
        gap_center = get_pipe_gap()
        temp.update(left, gap_center, pipe_gap)
        pipes.append(temp)

#Moves a sprite that is off the left off the screen to after the farthest right sprite
#This only works when the velocity is negative for the deque!
def deque_update(deque):
    if deque[0].isDead():
        left = deque[-1].get_right()
        top = deque[-1].get_top()
        temp = deque.popleft()
        temp.update(left, top)
        deque.append(temp)


def reset():
    bird.reset(bird_start_x, bird_start_y)
    scoreboard.update(0)
    reset_pipes()
    all_sprites.draw(game_display)
    pygame.display.update()

#Games States
def dead_state():
    #Automatically play the game
    if autoPlay:
        reset()
        return get_ready_state
    
    running = True
    while running:
        #Bird falls until it hits the ground
        if not pygame.sprite.spritecollide(bird, ground_sprites, False):
            bird_sprites.update()

        #Exit the dead screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        #Update the display
        draw_all_sprites()
        game_display.blit(gameover_image, gameover_image_rect)
        scoreboard.update()
        pygame.display.update()
        clock.tick(tick_rate)

    reset()
    return get_ready_state

def play_state():
    current_pipe = pipes[0] #Current pipe that the bird must fly through
    score = 0 #Keep track of the players score
    scoreboard.update(score)
    
    running = True
    while running:

        #Autoplay the game!
        if autoPlay:
            next_bottom_pos = bird.velocity + bird.get_bottom()
            if next_bottom_pos - current_pipe.get_bottoms_top() > 0:
                bird.tap()

        #Check if score should be increased and increase score if it should
        #Update the current pipe the bird must fly through
        if current_pipe.get_right() < bird.get_left():
            score += 1
            scoreboard.update(score)
            current_pipe = pipes[pipes.index(current_pipe) + 1]
        
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
        scoreboard.update()
        pygame.display.update()
        clock.tick(tick_rate)

        #If bird collides with the ground or a pipe, exit active game
        if pygame.sprite.spritecollide(bird, pipe_sprites, False) or pygame.sprite.spritecollide(bird, ground_sprites, False):
            bird.velocity = 0
            running = False

    return dead_state

def get_ready_state():
    #Automatically play the game
    if autoPlay:
        return play_state
    
    running = True
    while running:
        #Exit intro screen if any button is tapped or mouse button hit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                bird.tap()
                running = False

        #Update the pertinent sprites and display
        background_sprites.update()
        ground_sprites.update()
        deque_update(grounds)
        deque_update(backgrounds)
        draw_all_sprites()
        game_display.blit(tap_image, tap_image_rect)
        game_display.blit(getready_image, getready_image_rect)
        pygame.display.update()
        clock.tick(tick_rate)

    return play_state

def welcome_state():
    #Automatically play the game
    if autoPlay:
        return get_ready_state
    
    running = True
    while running:

        #Exit start screen if any button is tapped or mouse button hit
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.pressed(pygame.mouse.get_pos()):
                running = False

        #Update the pertinent sprites and display
        background_sprites.update()
        ground_sprites.update()
        deque_update(grounds)
        deque_update(backgrounds)
        background_sprites.draw(game_display)
        pipe_sprites.draw(game_display)
        ground_sprites.draw(game_display)
        start_button_sprite.draw(game_display)
        game_display.blit(start_image, start_image_rect)
        pygame.display.update()
        
        clock.tick(tick_rate)

    return get_ready_state

def play_game(next_state):
    running = True
    while running:
        if next_state == welcome_state:
            next_state = welcome_state()
        elif next_state == get_ready_state:
            next_state = get_ready_state()
        elif next_state == play_state:
            next_state = play_state()
        elif next_state == dead_state:
            next_state = dead_state()
        else:
            running = false

#Play the game!
play_game(welcome_state)

pygame.QUIT()
