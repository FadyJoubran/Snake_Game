# Imports
import pygame
import random

# Variables
SQUARE_SIZE = 30
BORDER_SIZE = 3
NOS = 21
NOB = NOS - 1
WIN_SIZE = NOS * SQUARE_SIZE + NOB * BORDER_SIZE
my_delay = 0
game_over = False

# Movement
up = False
down = False
left = False
right = False
change_dir = True

# Snake
head = pygame.Rect((NOS // 2) * SQUARE_SIZE + (NOS // 2) * BORDER_SIZE, (NOS // 2) * SQUARE_SIZE + (NOS // 2) * BORDER_SIZE, SQUARE_SIZE, SQUARE_SIZE)
tails = []
last_x = head.x
last_y = head.y

# Apple
apple = pygame.Rect(random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE), random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE), SQUARE_SIZE, SQUARE_SIZE)
while apple.x == head.x and apple.y == head.y:
    apple.x = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
    apple.y = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)

# Window
WIN = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
D_GREEN = (0, 123, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
snake_col = GREEN

# FPS
FPS = 60

# Function draw_window()
def draw_window():
    WIN.fill(BLACK)
    for i in range(NOB):
        pygame.draw.rect(WIN, WHITE, pygame.Rect((i + 1) * SQUARE_SIZE + i * BORDER_SIZE, 0, BORDER_SIZE, WIN_SIZE))
        pygame.draw.rect(WIN, WHITE, pygame.Rect(0, (i + 1) * SQUARE_SIZE + i * BORDER_SIZE, WIN_SIZE, BORDER_SIZE))
    for tail in tails:
        pygame.draw.rect(WIN, D_GREEN, tail)
    pygame.draw.rect(WIN, snake_col, head)
    pygame.draw.rect(WIN, RED, apple)
    
    pygame.display.update()

# Function delay()
def delay():
    global my_delay
    if not game_over:
        my_delay += 1
        if my_delay >= FPS // 10:
            my_delay = 0
            move()
            eat()
            collision()
            draw_window()
    else:
        my_delay += 1
        if my_delay >= FPS * 3:
            reset()


# Function update_movement()
def update_movement(event):
    global up, down, left, right, change_dir
    if event.key == pygame.K_UP and down == False and change_dir == True:
        up = True
        left = False
        right = False
        change_dir = False
    if event.key == pygame.K_DOWN and up == False and change_dir == True:
        down = True
        left = False
        right = False
        change_dir = False
    if event.key == pygame.K_LEFT and right == False and change_dir == True:
        left = True
        up = False
        down = False
        change_dir = False
    if event.key == pygame.K_RIGHT and left == False and change_dir == True:
        right = True
        up = False
        down = False
        change_dir = False

# Function move()
def move():
    global change_dir, last_x, last_y
    if len(tails) == 0:
        last_x = head.x
        last_y = head.y
    else:
        last_x = tails[-1].x
        last_y = tails[-1].y
    for i in range(len(tails) - 1, -1, -1):
        if i != 0:
            tails[i].x = tails[i-1].x
            tails[i].y = tails[i-1].y
        else:
            tails[0].x = head.x
            tails[0].y = head.y
    if up:
        head.y -= SQUARE_SIZE + BORDER_SIZE
    if down:
        head.y += SQUARE_SIZE + BORDER_SIZE
    if left:
        head.x -= SQUARE_SIZE + BORDER_SIZE
    if right:
        head.x += SQUARE_SIZE + BORDER_SIZE
    change_dir = True

# Function eat()
def eat():
    global last_x, last_y
    repeat = True
    if head.x == apple.x and head.y == apple.y:
        tails.append(pygame.Rect(last_x, last_y, SQUARE_SIZE, SQUARE_SIZE))
        while repeat:
            apple.x = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
            apple.y = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
            if apple.x != head.x or apple.y != head.y:
                repeat = False
                for tail in tails:
                    if apple.x == tail.x and apple.y == tail.y:
                        repeat = True

# Function collision()
def collision():
    global snake_col, game_over
    if head.x < 0 or head.y < 0 or head.x > WIN_SIZE or head.y > WIN_SIZE:
        snake_col = BLUE
        game_over = True
    for tail in tails:
        if head.x == tail.x and head.y == tail.y:
            snake_col = BLUE
            game_over = True

# Function reset()
def reset():
    global snake_col, up, down, left, right, game_over, my_delay
    head.x = (NOS // 2) * SQUARE_SIZE + (NOS // 2) * BORDER_SIZE
    head.y = (NOS // 2) * SQUARE_SIZE + (NOS // 2) * BORDER_SIZE
    apple.x = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
    apple.y = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
    while apple.x == head.x and apple.y == head.y:
        apple.x = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
        apple.y = random.randint(0, NOB) * (SQUARE_SIZE + BORDER_SIZE)
    snake_col = GREEN
    tails.clear()
    up = down = left = right = False
    game_over = False
    my_delay = 0


# Function main()
def main():
    clock = pygame.time.Clock()
    pause = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_SPACE:
                    pause = not pause
                elif pause == False:
                    update_movement(event)
        
        if pause == False:
            delay()
    
    pygame.quit()

# Run program
if __name__ == "__main__":
    main()