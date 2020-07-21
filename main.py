import pygame
import math
import random
from pygame import mixer

# pygame initilize
pygame.init()

# game screen size
screen = pygame.display.set_mode((800, 600))

# bakcground image
bckg=pygame.image.load('backgrd.png')

#bakground sound

mixer.music.load('background.wav')
mixer.music.play(-1)

# game icon and display
pygame.display.set_caption('Space_Mode')
icon = pygame.image.load('boy.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_chng = 0

# Enamy
enamiimg = []
enamiX=[]
enamiY=[]
enamiX_chng=[]
enamiY_chng=[]
num_of_enami=6

for i in range(num_of_enami):

    enamiimg.append(pygame.image.load('nk.png'))
    enamiX.append(random.randint(0,800))
    enamiY.append(random.randint(0,30))
    enamiX_chng.append(3)
    enamiY_chng.append(40)


#Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY=480
bulletY_chng=10
bullet_state='ready'

#score
score_value=0
font =pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game over text
over_font=pygame.font.Font('freesansbold.ttf',64)




def show_score(x,y):
    score = font.render('Score :' +str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render('Game Over.... :' , True, (255, 255, 255))
    screen.blit(over_text,(200,250))

def player(x, y):
    screen.blit(playerimg, (x, y))


def enami(x, y, i):
    screen.blit(enamiimg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+16,y+10))

def isColasion(enamiX,enamiY,bulletX,bulletY):
    distnc= math.sqrt((math.pow(enamiX-bulletX,2)) + (math.pow(enamiY-bulletY,2)))
    if distnc < 27:
        return True
    else :
        return False



# Gaming Loop
runnings = True
while runnings:

    # R G  B
    screen.fill((0, 0, 0))

    #bakcground
    screen.blit(bckg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnings = False

        # if key stork chack keybord

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_chng = -6
            if event.key == pygame.K_RIGHT:
                playerX_chng =6
            if event.key == pygame.K_UP:
                playerY_chng=-10

            if event.key==pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play(-1)
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_chng = 0


#BOundry of game
    playerX += playerX_chng

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Enami moving
    for i in range(num_of_enami):

        #Game over....
        if enamiY[i] > 440:
            for j in range(num_of_enami):
                enamiY[j]=20000
            game_over_text()
            break


        enamiX[i] += enamiX_chng[i]
        if enamiX[i] <= 0:
            enamiX[i] = 3
            enamiY[i]+=enamiY_chng[i]
        elif enamiX[i] >= 736:
            enamiX[i] = - 4
            enamiY[i]+=enamiY_chng[i]

        # collision..........
        collision = isColasion(enamiX[i], enamiY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()


            bulletY = 480
            bullet_state = 'ready'
            score_value+=1
            enamiX[i]=random.randint(0,800)
            enamiY[i]=random.randint(0,30)


        enami(enamiX[i],enamiY[i],i)




    if bulletY <= 0:
        bulletY=480
        bullet_state='ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_chng



    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
