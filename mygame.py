import pygame
import sys     # sys-module will be needed to exit the game
from pygame.locals import * # imports the constants of pygame
import Platform

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

# Surface objects can be added to the display surface with blit() method
# blit(Surface,(x,y)) adds "Surface" into coordinates (x,y)=(left, top)
dispSurf.blit(level, (0,0))

rectangle = Platform.Platform(960, 50, 0, 537, transp)
platfgroup = pygame.sprite.Group()
platfgroup.add(rectangle)
platform = Platform.Platform(220, 5, 460, 365, transp)
platfgroup.add(platform)

class Mario(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.left = 100
        self.rect.top = 250

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self,picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

# the display surface needs to be updated for the blitted Surfaces to become visible
# pygame.display.update() would do the same
pygame.display.flip()

mario = Mario("mario.png")
mario_group = pygame.sprite.Group()
mario_group.add(mario)

fireball = MovingSprite("fireball.png")
moving_group = pygame.sprite.Group()
moving_group.add(fireball)

# character physics
def fall():
    if not pygame.sprite.spritecollideany(mario, platfgroup) and not isJump:
        mario.rect.top += 1
        
isJump = False
speedx = 1
speedy = 20
jumpmax = 10

# speed contains the [x,y]-speed of the fireball in pixels
speed = [1,1]

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

    # fireball will be moved by speed=[1,1] in every iteration
    # move_ip([x,y]) changes the Rect-objects left-top coordinates by x and y
    fireball.rect.move_ip(speed)

    # fireball bounces from the edges of the display surface
    if fireball.rect.left < 0 or fireball.rect.right > width: # fireball is vertically outside the game
        speed[0] = -speed[0] # the x-direction of the speed will be converted
    if fireball.rect.top < 0 or fireball.rect.bottom > height: # fireball is horizontally outside the game
        speed[1] = -speed[1] # the y-direction of the speed will be converted

    # Fireball disappears after hitting the ground or platform
    if pygame.sprite.spritecollideany(fireball, platfgroup):
        fireball.kill()

    # get.pressed() function gives a boolean list of all the keys if they are being pressed
    pressings = pygame.key.get_pressed()
    if pressings[K_a]:          # if left-key is true in the list
        mario.rect.move_ip((-1,0))  # mario will be moved one pixel left
    if pressings[K_d]:
        mario.rect.move_ip((1,0))
      
    if isJump == False and pygame.sprite.spritecollideany(mario, platfgroup) and pressings[K_SPACE]:
        isJump = True

    if isJump == True:
        mario.rect.top -= speedy
        jumpmax -= 1
        if jumpmax < 0:
            isJump = False
            jumpmax = 10

    fall()

    # blit all the Surfaces in their new places
    dispSurf.blit(level, (0,0)) # without this, moving characters would have a "trace"
    moving_group.draw(dispSurf)
    mario_group.draw(dispSurf)
    platfgroup.draw(dispSurf)

    pygame.time.delay(3)
    # updating the display surface is always needed at the end of each iteration of game loop
    pygame.display.flip()

