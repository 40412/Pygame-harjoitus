import pygame, ScreenObject, sys
from pygame.locals import * # imports the constants of pygame
from ScreenObject import *
import random as r
from math import *
import functionality as fun

pygame.init()  # initializes pygame

# the display surface
width = 960
height = 600
dispSurf = pygame.display.set_mode((width,height))
pygame.display.set_caption("My game")

# the Surface objects
level = pygame.image.load("level.jpg").convert()
# pygame.image.load(file) function loads a picture "file" into a given variable
# convert() method converts the picture into the right pixel-format
# picture files needs to be in the same folder as this python file
# the folder path can be relative or absolute:
# relative path: mario = pygame.image.load("folder\\mario.png").convert()
# absolute path: fireball = pygame.image.load("C:\\folder\\fireball.png").convert()

# RGB-colors are tuples (r,g,b), where 0<r,g,b<255
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,0,130)
transp = (0,0,0,0)

#Different groups to handle sprites
platfgroup = pygame.sprite.Group()
mario_group = pygame.sprite.Group()
moving_group = pygame.sprite.Group()
headcollision_group = pygame.sprite.Group()
sidecollision_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

# Surface objects can be added to the display surface with blit() method
# blit(Surface,(x,y)) adds "Surface" into coordinates (x,y)=(left, top)
dispSurf.blit(level, (0,0))

#Sprites
rectangle = ScreenObject.Platform(width, 50, 0, 537, transp)
platfgroup.add(rectangle)
platform = ScreenObject.Platform(220, 5, 460, 365, transp)
platfgroup.add(platform)
pipe = ScreenObject.MovingSprite("Pipe.png", 850, height - 110)
sidecollision_group.add(pipe)
pipetop = ScreenObject.Platform(40, 150, 830, height- 150, transp)
platfgroup.add(pipetop)
qmark1top = ScreenObject.Platform(45, 5, 287, 360, transp)
platfgroup.add(qmark1top)
qmark2top = ScreenObject.Platform(40, 5, 550, 190, transp)
platfgroup.add(qmark2top)
mario = ScreenObject.Mario("marioAlpha.png")
mario_group.add(mario)
fireball = ScreenObject.MovingSprite("fireball.png", 100, 50)
fireball.image.set_colorkey((0,0,255), 0)
moving_group.add(fireball)
qmarkbox1 = ScreenObject.Platform(45, 5, 287, 400, transp)
headcollision_group.add(qmarkbox1)
qmarkbox2 = ScreenObject.Platform(40, 5, 550, 230, transp)
headcollision_group.add(qmarkbox2)
tiles = ScreenObject.Platform(220, 5, 460, 400, transp)
headcollision_group.add(tiles)
qmarkbox1side = ScreenObject.Platform(45,25, 287, 370, transp)
sidecollision_group.add(qmarkbox1side)
qmarkbox2side = ScreenObject.Platform(40, 25, 550, 200, transp)
sidecollision_group.add(qmarkbox2side)
tilesside = ScreenObject.Platform(220, 25, 460, 370, transp)
sidecollision_group.add(tilesside)
crosshair = pygame.draw.circle(dispSurf, white, pygame.mouse.get_pos(), 3, 2)

# If mario touches the fireball, he loses health.
# This function empties the heart_group and checks the current health situation and updates the group
def update_hearts():
    heart_group.empty()
    heartpos = 50
    for i in range(mario.health):
        heartpos += 50
        heart = ScreenObject.MovingSprite("heart.png", heartpos, 50)
        heart_group.add(heart)
# the display surface needs to be updated for the blitted Surfaces to become visible
# pygame.display.update() would do the same
pygame.display.flip()

isJump = False
controls = True
speedx = 2
speedy = 10
x_direct_right = False
jumpmax = 25
clock = pygame.time.Clock()
boom = pygame.mixer.Sound("boom.wav")
gameoverfont = pygame.font.SysFont('arial', 80)
gameovertext = gameoverfont.render('GAME OVER', True, red)

# speed contains the [x,y]-speed of the fireball in pixels
speed = [r.randint(0,1),1]

update_hearts()
pygame.mouse.set_visible(False)

bullets = []

# the game loop which runs until sys.exit()
while True:
    # loop to check if the user has closed the display window or pressed esc
    for event in pygame.event.get():  # list of all the events in the event queue
        if event.type == pygame.QUIT: # if the player closed the window
            pygame.quit() # the display window closes
            sys.exit()    # the python program exits
        if event.type == KEYDOWN:     # if the player pressed down any key
            if event.key == K_ESCAPE: # if the key was esc
                pygame.quit() # the display window closes
                sys.exit()    # the python program exits
    
    if pygame.sprite.spritecollideany(fireball, mario_group):
        mario.update()
        update_hearts()

    if mario.isalive == False:
        dispSurf.blit(gameovertext, (300, 250))
        pygame.display.update()
        pygame.time.wait(5000)
        sys.exit()
    fun.fireball_movement(fireball, width, height, speed, platfgroup, mario_group)
    fun.fb_collision(fireball, platfgroup, mario_group, speed)
    
    pressings = pygame.key.get_pressed()
    fun.key_pressings(mario, controls, speedx, x_direct_right)

    #Shooting bullets if mousebutton is clicked
    if event.type == MOUSEBUTTONDOWN:
        bullet = ScreenObject.Bullet(mario.rect.center, fun.get_angle(pygame.mouse.get_pos(), mario.rect.center))
        bullets.append(bullet)
      
    if isJump == False and pygame.sprite.spritecollideany(mario, platfgroup) and pressings[K_SPACE]:
        isJump = True

    if isJump == True:
        if pygame.sprite.spritecollideany(mario, headcollision_group):
            speedy = 0
            isJump = False
        else:
            mario.rect.top -= speedy
            jumpmax -= 1
            if jumpmax < 0:
                isJump = False
                jumpmax = 25
        speedy = 10
    fun.fall(mario, platfgroup, isJump)
    fun.map_edges(mario, width)
    fun.collisions(mario, sidecollision_group, controls, speedx, x_direct_right)
    fun.pipejump(pipetop, mario_group, mario, pipe, height, controls)
    # Draw all the Surfaces
    dispSurf.blit(level, (0,0)) # without this, moving characters would have a "trace"
    for bullet in bullets:
        bullet.draw_bullet(dispSurf)
        bullet.update()
    moving_group.draw(dispSurf)
    mario_group.draw(dispSurf)
    platfgroup.draw(dispSurf)
    headcollision_group.draw(dispSurf)
    sidecollision_group.draw(dispSurf)
    heart_group.draw(dispSurf)
    pygame.draw.circle(dispSurf, white, pygame.mouse.get_pos(), 10, 2)

    clock.tick(250)
    # updating the display surface is always needed at the end of each iteration of game loop
    pygame.display.flip()