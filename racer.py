#1 Racer
#Imports
import pygame, sys

from pygame.locals import *
import random, time
 
#Initialzing 
pygame.init()
pygame.mixer.init()

 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0 #for counting score
COIN_SPEED = 5
count = 0 #for counting numbers of coins
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("AnimatedStreet.png")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1) 

 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
#creating coins
class Coin:
    def __init__(self):
        self.radius = 10
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = -50
        self.speed = COIN_SPEED
    def move(self):
        self.y+=self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset_position()
    def reset_position(self):
        self.y = -50
    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,0), (self.x, self.y), self.radius)




#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    counts = font_small.render(f"Coins: {str(count)}", True, BLACK)
    DISPLAYSURF.blit(counts, (SCREEN_WIDTH-110,10 )) #the place of the coin amounts
    

    C1.move()
    C1.draw(DISPLAYSURF)
    
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if hasattr(entity, "move"):  # Проверяем, есть ли метод move
            entity.move()

    
   #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit() 
    
    if P1.rect.colliderect(pygame.Rect(C1.x - C1.radius, C1.y - C1.radius, C1.radius * 2, C1.radius * 2)):
        count += 1  # We give you more points for a coin
        C1.reset_position() 
    
           
    pygame.display.update()
    FramePerSec.tick(FPS)