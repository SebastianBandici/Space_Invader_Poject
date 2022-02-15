import math
import pygame
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode ((800,600))

# Background
background = pygame.image.load('wepik-202207-344.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("     SPACE INVADER")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 4

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('alien2.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
# ready bullet_state = you can't see the bullet on the screen
# fire bullet_state = the bullet is currently moving
bullet_state = "ready"

# Game Over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_text, (250, 250))

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255,255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))



def isCollision(enemyX, enemyY, bulletX, bullety):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bullety, 2))
    if distance < 27:
        return  True
    else:
        return False

# Game loop
running = True
while running:
    # RGB color - Red, Green, Blue
    # screen.fill(155, 0, 0)

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right of left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0




    playerX += playerX_change

    # Creating SpaceShip boundaries so it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement
    for i in range(number_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480;
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Display Player
    player(playerX, playerY)

    # Display Score
    show_score(textX, textY)

    pygame.display.update()

