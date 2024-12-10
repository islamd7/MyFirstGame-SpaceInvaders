import pygame
import math
import random
from pygame import mixer

#Initialize pygame
pygame.init()

#Screen
screen = pygame.display.set_mode((800,600))
is_fullscreen = False

#TItle and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.ico")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("background.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
nums_of_enemies = 6

for i in range (nums_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(0.3 or -0.3)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"


#Player
playerImg = pygame.image.load("spaceinvaders.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
score_color = 0,0,0

#Game over
over_text_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_text_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (score_color))
    screen.blit(score, (x,y))

#Game running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
    #Movement buttons
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerX_change = -0.4
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerX_change = 0.4
    else:
        playerX_change = 0
    if keys[pygame.K_F11]:
        if not is_fullscreen:
            pygame.display.set_mode((800,600),pygame.FULLSCREEN)
            is_fullscreen = True
        else:
            pygame.display.set_mode((800,600))
            is_fullscreen = False
        
    #Background color
    screen.fill((150,255,255))

    #Background image
    screen.blit(background,(0,0))

    #Player movement
    playerX += playerX_change

    #Boundary
    if playerX <=0:
        playerX = 0
    if playerX >=736:
        playerX = 736



    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bulletY_change
        

    #Enemy movement
    for i in range (nums_of_enemies):
        if enemyY[i] > 440:
            for j in range (nums_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #Collision = Çarpışma
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision is True:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,100)
        enemy(enemyX[i],enemyY[i],i)

    if score_value == 30:
        score_color = 0,255,0
    elif score_value == 50:
        score_color = 255,0,0

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()