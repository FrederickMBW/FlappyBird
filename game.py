import pygame
import random
pygame.init()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bird2.jpg").convert_alpha()

        self.rect = self.image.get_rect()
        self.speed_x = 0

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

        
class Pipe(pygame.sprite.Sprite):
   def __init__(self, width, height):
       super().__init__()
       self.image = pygame.Surface((width, height))
       self.image.fill((0,200,30))
       #self.image = pygame.image.load("pillar.jpg")
       self.rect = self.image.get_rect()
   def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


screenWidth = 500
screenHeight = 500
game_display = pygame.display.set_mode((screenWidth,screenHeight))

all_sprites = pygame.sprite.Group()

bird = Bird()
bird.speed_x = 1
shortPipe = Pipe(50, 100)
longPipe = Pipe(50, 300) 
shortPipe2 = Pipe(50, 100)
longPipe2 = Pipe(50, 300)

pipes = pygame.sprite.Group()
pipes.add(shortPipe)
pipes.add(longPipe)
pipes.add(shortPipe2)
pipes.add(longPipe2)

shortPipe2.update(400, 0)
longPipe2.update(400,300)

all_sprites.add(bird)
all_sprites.add(pipes)


pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

#image = pygame.image.load("bird2.jpg")
#pillar = pygame.image.load("pillar.jpg")
#def drawRect(x, y, width, height):
#    pygame.draw.rect(display, (0,255,0), (x,y,width,height),2)

crashed = False
white = (255, 255, 255)

font = pygame.font.SysFont("comicsansms",24)
#text = font.render("Hello World", True, (0,123,234))
    
upper_xp = 200
upper_yp = 0

lower_xp = 200
lower_yp = 400

upper_xp2 = 400
upper_yp2 = 0

lower_xp2 = 400
lower_yp2 = 400

x = 20
y = 10
y2 = 0
while not crashed:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            crashed = True
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                y2 = -20
            elif(event.key == pygame.K_DOWN):
               y2 = 20
        #elif(event.type == pygame.KEYUP):
            #if(event.key == pygame.K_UP or event.key == pygame.K_DOWN):
    
    if y2 == 0:
        y += 1
    else:
        y += y2
    y2 = 0

    upper_xp -= 1
    lower_xp -= 1
    upper_xp2 -= 1
    lower_xp2 -= 1

    if (upper_xp == 0):
        upper_yp = random.randint(-20,0)
        upper_xp = screenWidth
    if (lower_xp == 0):
        lower_yp = random.randint(200,400)
        lower_xp = screenWidth
    if (upper_xp2 == 0):
        upper_yp2 = random.randint(-20,0)
        upper_xp2 = screenWidth
    if (lower_xp2 == 0):
        lower_yp2 = random.randint(200,400)
        lower_xp2 = screenWidth
    
    game_display.fill(white)

    longPipe.update(lower_xp, lower_yp)
    shortPipe.update(upper_xp, upper_yp)
    longPipe2.update(lower_xp2, lower_yp2)
    shortPipe2.update(upper_xp2, upper_yp)
    #pipeBottom2.update(lower_xp2, lower_yp)
    #pipeTop2.update(upper_xp2, upper_yp)
    bird.update(x, y)
    #game_display.blit(text, (20,20))
    all_sprites.draw(game_display)

    pygame.display.update()
    clock.tick(60)

    if pygame.sprite.spritecollide(bird, pipes, True):
        print ("Game Over")
        crashed = True
    
    
pygame.quit()
quit()
