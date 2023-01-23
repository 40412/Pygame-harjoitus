import pygame
import sys     # sys-module will be needed to exit the game
from pygame.locals import * # imports the constants of pygame
import ScreenObject
import random as r

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

# character physics
def fall():
    if not pygame.sprite.spritecollideany(mario, platfgroup) and not isJump:
        mario.rect.top += 2

def map_edges():
    if mario.rect.centerx > width:
        mario.rect.centerx = 0
    if mario.rect.centerx < 0:
        mario.rect.centerx = width
        
isJump = False
controls = False
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

# the game loop which runs until sys.exit()
while True:
    pygame.mouse.set_visible(False)
    # loop to check if the user has closed the display window or pressed esc
    for event in pygame.event.get():  # list of all the events in the event queue
        if event.type == pygame.QUIT: # if the player closed the window
            pygame.quit() # the display window closes
            sys.exit()    # the python program exits
        if event.type == KEYDOWN:     # if the player pressed down any key
            if event.key == K_ESCAPE: # if the key was esc
                pygame.quit() # the display window closes
                sys.exit()    # the python program exits
    # fireball will be moved by speed=[1,1] in every iteration
    # move_ip([x,y]) changes the Rect-objects left-top coordinates by x and y
    fireball.rect.move_ip(speed)
    # fireball bounces from the edges of the display surface
    if fireball.rect.left < 0 or fireball.rect.right > width: # fireball is vertically outside the game
        speed[0] = -speed[0] # the x-direction of the speed will be converted
    if fireball.rect.top < 0 or fireball.rect.bottom > height: # fireball is horizontally outside the game
        speed[1] = -speed[1] # the y-direction of the speed will be converted

    if pygame.sprite.spritecollideany(fireball, mario_group):
        mario.update()
        update_hearts()

    if mario.isalive == False:
        dispSurf.blit(gameovertext, (300, 250))
        pygame.display.update()
        pygame.time.wait(5000)
        sys.exit()

    # Fireball disappears after hitting the ground or platform
    if pygame.sprite.spritecollideany(fireball, platfgroup) or pygame.sprite.spritecollideany(fireball, mario_group):
        boom.play()
        fireball.update()
        speed[0] = r.randint(-1,1)

    # get.pressed() function gives a boolean list of all the keys if they are being pressed
    pressings = pygame.key.get_pressed()
    if pressings[K_a] and controls:          # if left-key is true in the list
        mario.rect.move_ip((-1 * speedx,0))  # mario will be moved one pixel left
        x_direct_right = False
    if pressings[K_d] and controls:
        mario.rect.move_ip((speedx,0))
        x_direct_right = True
      
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

    fall()
    map_edges()

    if pygame.sprite.spritecollideany(mario, sidecollision_group):
        speedx = 0
        if x_direct_right == True:
            mario.rect.move_ip(-5,0)
        if x_direct_right == False:
            mario.rect.move_ip(5,0)
    else:
        speedx = 2

    #if mario touches the top of the pipe, he jumps inside it
    if pygame.sprite.spritecollideany(pipetop, mario_group):
        controls = False
        mario.rect.centerx = pipe.rect.centerx
        mario.rect.top += 1
        if mario.rect.center[1] > height-110:
            mario.rect.center = 100, 0
    else: controls = True

    # blit all the Surfaces in their new places
    dispSurf.blit(level, (0,0)) # without this, moving characters would have a "trace"
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