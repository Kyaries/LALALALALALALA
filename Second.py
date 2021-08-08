import pygame
import random
import math
from pygame import mixer

pygame.init()

# Window Display
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("Background.jpg")

mixer.music.load("background.wav")
mixer.music.play(-1)
# Player

playership = pygame.image.load("space ship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Aliens
alien_enemy = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_alien = 6

for i in range(num_of_alien):
    alien_enemy.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(1, 735))
    alienY.append(random.randint(20, 50))
    alienX_change.append(0.3)
    alienY_change.append(20)

# Bullet
bullet_move = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 445
bulletY_change = 2
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
fontX = 10
fontY = 10

failed_font = pygame.font.Font("freesansbold.ttf", 64)


# Function

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def show_failed():
    failed = failed_font.render("GAME OVER", True, (255, 255, 255))
    window.blit(failed, (200, 250))


def player(x, y):
    window.blit(playership, (x, y))


def alien(x, y, i):
    window.blit(alien_enemy[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bullet_move, (x + 16, y))


def iscollide(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop
running = True
while running:
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.8
            if event.key == pygame.K_d:
                playerX_change = +0.8
            if event.key == pygame.K_w:
                playerY_change = -0
            if event.key == pygame.K_s:
                playerY_change = +0
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_change = 0
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    if bulletY <= 0:
        bulletY = 445
        bullet_state = "ready"

    for i in range(num_of_alien):
        if alienY[i] > 200:
            for j in range(num_of_alien):
                alienY[j] = 2000
            show_failed()
            break
        alienX[i] += alienX_change[i]

        if alienX[i] >= 736:
            alienX[i] = 736
            alienY[i] += alienY_change[i]
            alienX_change[i] = -0.3
        elif alienX[i] <= 0:
            alienX[i] = 0
            alienY[i] += alienY_change[i]
            alienX_change[i] = 0.3

        collide = iscollide(alienX[i], alienY[i], bulletX, bulletY)
        if collide:
            death_sound = mixer.Sound("explosion.wav")
            death_sound.play()
            bulletY = 445
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(1, 735)
            alienY[i] = random.randint(20, 50)
        alien(alienX[i], alienY[i], i)

    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    playerY += playerY_change
    playerX += playerX_change
    show_score(fontX, fontY)
    player(playerX, playerY)
    pygame.display.update()
