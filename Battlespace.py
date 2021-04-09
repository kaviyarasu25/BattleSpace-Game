import pygame
from pygame import mixer
import random
import math

#intiate the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((700,400))

#Background
background = pygame.image.load('background_pygame.png')

#change Title and Icon
pygame.display.set_caption("BattleSpace")

icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)
battleship = pygame.image.load('battleship.png')

#player1 
player1 = pygame.image.load('battleship.png')
player1x = 300
player1y = 300
playerchangex = 0
#playerchangey = 0

#Enemy1
enemyimg = []
enemyx = []
enemyy = []
enemychangex = []
enemychangey = []

no_of_enemies = 6

for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,636))
    enemyy.append(random.randint(0,30))
    enemychangex.append(0.5)
    enemychangey.append(10)

#Bullet
bullet = pygame.image.load('bullet.png')
bulletx = 0
bullety = 300
bulletchangex = 0
bulletchangey = 1
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('TrainOne-Regular.ttf',20)
textx = 10
texty = 10

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Game Over
over_font = pygame.font.Font('Anton-Regular.ttf',50)

def game_over_text():
    over = over_font.render("GAME OVER",True,(225,225,225))
    screen.blit(over, (240,150))

def show_score(x,y):
    score = font.render("Score : " +str(score_value),True,(225,225,225))
    screen.blit(score, (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet,(x + 15,y +6))


def p1(x,y):
    screen.blit(player1,(x,y))

def e1(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def iscollision(enemyx,enemyy,bulletx,bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx,2)) + (math.pow(enemyy-bullety,2)))
    if distance < 20:
        return True
    
    return False


running = True

#screen loop
while running:
    # screen color R-red B-blue G-green
    screen.fill((0,0,0))
    #Background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

        #check whether if keystroke pressed is Right or Left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchangex = -0.5
            if event.key == pygame.K_RIGHT:
                playerchangex =0.5
            """if event.key == pygame.K_UP:
                playerchangey = -0.3
            if event.key == pygame.K_DOWN:
                playerchangey = 0.3 """
            
            #Bullet
            if bullet_state is "ready":
                if event.key == pygame.K_SPACE:
                    #Bullet Sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    bulletx = player1x
                    fire_bullet(bulletx,bullety)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 playerchangex = 0
            
            #if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 #playerchangey = 0
                
                
    #(Explanation)
    # 300 = 300 + (-0.3) ->300 = 300 - 0.3
    # 300 = 300 + 0.3
    player1x +=playerchangex
  
   # player1y += playerchangey

    #Boundaries for the battleship in screen
    if player1x <=0:
        player1x=0
    elif player1x >=636:
        player1x=636
    """if player1y <=0:
        player1y = 0
    elif player1y >= 336:
        player1y = 336 """

    #Boundaries for the enemy in screen

    for i in range(no_of_enemies):
        if enemyy[i] >235:
            for j in range(no_of_enemies):
                enemyy[j] = 1000
            game_over_text()
        enemyx[i] +=enemychangex[i]
        if enemyx[i] <=0:
            enemyy[i] += enemychangey[i]
            enemychangex[i] = 0.5
        elif enemyx[i] >=636:
            enemyy[i] += enemychangey[i]
            enemychangex[i] = -0.5
            
        
        
        #collision
        collision = iscollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            #Collision Sound
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 300
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0,600)
            enemyy[i] = random.randint(0,30)
            
        
        e1(enemyx[i],enemyy[i],i)

    
    #Bullet Movement
    if bullety <=0:
        bullety = 300
        bullet_state = 'ready'

    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bulletchangey 
    

    p1(player1x,player1y)
    show_score(textx,texty)
    pygame.display.update()
    
    
