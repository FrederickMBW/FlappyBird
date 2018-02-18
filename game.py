import pygame
import random
pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bird.png").convert_alpha()

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


speed = 1
screenWidth = 800
screenHeight = 500
game_display = pygame.display.set_mode((screenWidth,screenHeight))

BackGround = Background('background.jpg', [0,0])
all_sprites = pygame.sprite.Group()

bird = Bird()
bird.speed_x = 1
shortPipe = Pipe(50, 200)
longPipe = Pipe(50, 400) 
shortPipe2 = Pipe(50, 200)
longPipe2 = Pipe(50, 400)
shortPipe3 = Pipe(50, 200)
longPipe3 = Pipe(50, 400)

pipes = pygame.sprite.Group()
pipes.add(shortPipe)
pipes.add(longPipe)
pipes.add(shortPipe2)
pipes.add(longPipe2)
pipes.add(shortPipe3)
pipes.add(longPipe3)

shortPipe2.update(400, 0)
longPipe2.update(400,300)

shortPipe3.update(800, 0)
longPipe3.update(800,300)

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
oupper_yp = 0

lower_xp = 200
lower_yp = 400
olower_yp = 400

upper_xp2 = 500
upper_yp2 = 0
oupper_yp2 = 0

lower_xp2 = 500
lower_yp2 = 400
olower_yp2 = 400

upper_xp3 = 800
upper_yp3 = 0
oupper_yp3 = 0

lower_xp3 = 800
lower_yp3 = 400
olower_yp3 = 400

x = 20
y = 10
y2 = 0
lapCntr = 0
while not crashed:
    game_display.fill([255, 255, 255])
    game_display.blit(BackGround.image, BackGround.rect)
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

    upper_xp -= speed
    lower_xp -= speed
    upper_xp2 -= speed
    lower_xp2 -= speed
    upper_xp3 -= speed
    lower_xp3 -= speed

    adjust = random.randint(0,200)
    adjust2 = random.randint(50,100)

    if (upper_xp == 0):
        upper_yp = oupper_yp - adjust
        upper_xp = screenWidth
#    if (lower_xp == 0):
        lower_yp = olower_yp - adjust
        lower_xp = screenWidth
    if (upper_xp2 == 0):
        upper_yp2 = oupper_yp2 - adjust2
        upper_xp2 = screenWidth
#    if (lower_xp2 == 0):
        lower_yp2 = olower_yp2 - adjust2
        lower_xp2 = screenWidth
    if (upper_xp3 == 0):
        upper_yp3 = oupper_yp2 - adjust2
        upper_xp3 = screenWidth
#    if (lower_xp2 == 0):
        lower_yp3 = olower_yp2 - adjust2
        lower_xp3 = screenWidth
        lapCntr += 1
        if(lapCntr > 2):
            speed += 1
            lapCntr = 0
    
    #game_display.fill(white)

    longPipe.update(lower_xp, lower_yp)
    shortPipe.update(upper_xp, upper_yp)
    longPipe2.update(lower_xp2, lower_yp2)
    shortPipe2.update(upper_xp2, upper_yp2)
    longPipe3.update(lower_xp3, lower_yp3)
    shortPipe3.update(upper_xp3, upper_yp3)
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
