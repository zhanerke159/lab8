#2 snake
import pygame
import random

pygame.init()

w, h = 800, 800
BLOCK_SIZE = 50
font = pygame.font.Font(None, 100)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake game")
clock = pygame.time.Clock()
run = True

def drawGrid():#creating cells
    for x in range(0, w, BLOCK_SIZE):
        for y in range(0, h, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1) 

class Snake: #creating snake
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False

    def update(self): 
        global apple, start, lev
        for square in self.body:
            if square.x == self.head.x and square.y == self.head.y:
                self.dead = True

        if self.head.x < 0 or self.head.x >= w or self.head.y < 0 or self.head.y >= h:
            self.dead = True

        if self.dead:
            self.__init__()
            apple = Apple()
            start = 0  
            lev = 1  

        self.body.append(self.head.copy())  
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.pop(0)  

class Apple: #creating food
    def __init__(self): #random appearance of food
        self.x = random.randint(0, (w // BLOCK_SIZE) - 1) * BLOCK_SIZE 
        self.y = random.randint(0, (h // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

start = 0  #count score
lev = 1 #count level
speed = 10
snake = Snake()
apple = Apple()

while run:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.ydir = 1
                snake.xdir = 0   
            elif event.key == pygame.K_UP and snake.ydir == 0:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()
    drawGrid()
    apple.update()

    score = font.render(f"{start}", True, (0, 0, 0))
    score_pos = score.get_rect(center=(w / 2, h / 20))       #location of score
    screen.blit(score, score_pos)

    level = font.render(f"{lev} level", True, (0, 0, 0))
    level_pos = level.get_rect(center=(w / 2, h / 8))      #location of level
    screen.blit(level, level_pos)

    pygame.draw.rect(screen, (255, 255, 0), snake.head)
    
    for sq in snake.body:
        pygame.draw.rect(screen, (0, 255, 0), sq)

    
    if snake.head.x == apple.x and snake.head.y == apple.y: #snake lengthening
        last_part = snake.body[-1]
        snake.body.append(pygame.Rect(last_part.x, last_part.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()
        start += 1  
        if start % 4 == 0:
            lev += 1
            speed+=2

    pygame.display.update()
    clock.tick(speed)

pygame.quit()