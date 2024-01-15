from os import kill
from turtle import delay
import pygame
import time 
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 100
PLAYER_VELOCITY = 5

METEOR_WIDTH = 90
METEOR_HEIGHT = 90

clock = pygame.time.Clock()
start_time = time.time()
elapsed_time = 0 

FONT = pygame.font.SysFont('Consolas', 30)

meteors = []  # List to store the meteors
meteor_delay = 2  # Delay between meteor spawns in seconds
last_meteor_time = time.time()  # Time of the last meteor spawn

meteor_delay = 2  # Add the meteor_delay as a global variable

def create_meteor():
    global last_meteor_time
    global meteor_delay
    current_time = time.time()
    if current_time - last_meteor_time >= meteor_delay:
        num_meteors = 1  # Increase the number of meteors every 10 seconds
        meteor_x = random.randint(0, WIDTH - METEOR_WIDTH)
        meteor_y = -90
        meteors.append((meteor_x, meteor_y))
        meteor_x = random.randint(0, WIDTH - METEOR_WIDTH)
        meteor_y = -90
        meteors.append((meteor_x, meteor_y))
        for _ in range(num_meteors):
            meteor_x = random.randint(0, WIDTH - METEOR_WIDTH)
            meteor_y = -90
            meteors.append((meteor_x, meteor_y))
            num_meteors += 1
            if (current_time%10 == 0):
                num_meteors += 1
            print(num_meteors)
            
        last_meteor_time = current_time
        if meteor_delay>=0.7:
            meteor_delay *= 0.98

def move_meteors():
    for i in range(len(meteors)):
        meteor_x, meteor_y = meteors[i]
        meteor_y += 5  # Move the meteor downwards
        meteors[i] = (meteor_x, meteor_y)

def draw_meteors(meteor):
    for meteor_x, meteor_y in meteors:
        WIN.blit(meteor, (meteor_x, meteor_y))

def draw(player, PLAYERX, PLAYERY, elapsed_time, meteor, MeteorY):
    WIN.blit(BG, (0, 0))
    timer = FONT.render("time: " + str(round(elapsed_time)) + "s", True, "white")
    meteors_destroyed_text = FONT.render("Meteors Destroyed: " + str(meteors_destroyed), True, "white")
    WIN.blit(meteors_destroyed_text, (WIDTH - meteors_destroyed_text.get_width() - 10, 10))
    WIN.blit(timer, (10, 10))
    WIN.blit(player, (PLAYERX, PLAYERY))
    for bullet_x, bullet_y in bullets:
        pygame.draw.rect(WIN, (255, 255, 255), (bullet_x, bullet_y, 5, 10))
    draw_meteors(meteor)  # Call the new function to draw the meteors
    pygame.display.update()

def check_collision(PLAYERX, PLAYERY, PLAYER_HEIGHT, MeteorY, METEOR_HEIGHT):
    for meteor_x, meteor_y in meteors:
        if PLAYERX + PLAYER_WIDTH/2 >= meteor_x and PLAYERX <= meteor_x + METEOR_WIDTH/2:
            if PLAYERY + PLAYER_HEIGHT/2 >= meteor_y and PLAYERY <= meteor_y + METEOR_HEIGHT/2:
                return True
    return False

def game_over(score):
    game_over_text = FONT.render("Game Over", True, "white")
    score_text = FONT.render("Score: " + str(score)+"s", True, "white")
    WIN.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()))
    WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2))
    pygame.display.update()
    time.sleep(3)
bullets = []
BULLET_VELOCITY = 10

def create_bullet(PLAYERX, PLAYERY):
    bullet_x = PLAYERX + PLAYER_WIDTH/2
    bullet_y = PLAYERY
    bullets.append((bullet_x, bullet_y))

def move_bullets():
    for i in range(len(bullets)):
        bullet_x, bullet_y = bullets[i]
        bullet_y -= BULLET_VELOCITY  # Move the bullet upwards
        bullets[i] = (bullet_x, bullet_y)

 
meteors_destroyed = 0
def check_bullet_collision(meteors_destroyed):
    for bullet_x, bullet_y in bullets:
        for meteor_x, meteor_y in meteors:
            if bullet_x >= meteor_x and bullet_x <= meteor_x + METEOR_WIDTH:
                if bullet_y >= meteor_y and bullet_y <= meteor_y + METEOR_HEIGHT:
                    bullets.remove((bullet_x, bullet_y))
                    meteors.remove((meteor_x, meteor_y))
                    meteors_destroyed += 1
                    return
def main():
    run = True
    player = pygame.transform.scale(pygame.image.load("spaceship.PNG"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    meteor = pygame.transform.scale(pygame.image.load("meteor.png"),(METEOR_WIDTH,METEOR_HEIGHT))
    PLAYERX = 500
    PLAYERY = 600
    MeteorY = 0
    score = 0
    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and PLAYERX >= 0:
            PLAYERX -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and PLAYERX <= WIDTH - PLAYER_WIDTH:
            PLAYERX += PLAYER_VELOCITY
        if keys[pygame.K_UP] and PLAYERY >= 0:
            PLAYERY -= PLAYER_VELOCITY
        if keys[pygame.K_DOWN] and PLAYERY <= HEIGHT - PLAYER_HEIGHT:
            PLAYERY += PLAYER_VELOCITY
        if keys[pygame.K_SPACE]and round(elapsed_time)%2==0:
            create_bullet(PLAYERX,PLAYERY)
            
        
        move_bullets()
        check_bullet_collision(meteors_destroyed)
        

        create_meteor()
        move_meteors()

        if check_collision(PLAYERX, PLAYERY, PLAYER_HEIGHT, MeteorY, METEOR_HEIGHT):
            run = False
            game_over(round(elapsed_time))

        draw(player, PLAYERX, PLAYERY, elapsed_time, meteor, MeteorY)  # Move draw function inside the loop to update the screen

       

    pygame.quit()


if __name__ == "__main__":
    main()
