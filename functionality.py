import ScreenObject, sys, pygame
from pygame.locals import *
from math import *
import random as r

def fall(mario, platfgroup, isJump):
    if not pygame.sprite.spritecollideany(mario, platfgroup) and not isJump:
        mario.rect.top += 2

def jump(mario, headcollision_group, platfgroup): #not working!
    isJump = False
    jumpmax = 25
    speedy = 10
    pressings = pygame.key.get_pressed()
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

def map_edges(mario, width):
    if mario.rect.centerx > width:
        mario.rect.centerx = 0
    if mario.rect.centerx < 0:
        mario.rect.centerx = width

def get_angle(point2, point1):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        angle = atan2(dy, dx)
        return angle

def key_pressings(mario, controls, speedx, x_direct_right):
     # get.pressed() function gives a boolean list of all the keys if they are being pressed
    pressings = pygame.key.get_pressed()
    if pressings[K_a] and controls:          # if left-key is true in the list
        mario.rect.move_ip((-1 * speedx,0))  # mario will be moved one pixel left
        x_direct_right = False
    if pressings[K_d] and controls:
        mario.rect.move_ip((speedx,0))
        x_direct_right = True

def collisions(mario, sidecollision_group, controls, speedx, x_direct_right):
    if pygame.sprite.spritecollideany(mario, sidecollision_group):
        speedx = 0
        pressings = pygame.key.get_pressed()
        if pressings[K_d] and controls:
            x_direct_right = True
        if pressings[K_a] and controls:
            x_direct_right = False
        if x_direct_right == True:
            mario.rect.move_ip(-5,0)
        if x_direct_right == False:
            mario.rect.move_ip(5,0)
    else:
        speedx = 2

def pipejump(pipetop, mario_group, mario, pipe, height, controls):
    #if mario touches the top of the pipe, he jumps inside it
    if pygame.sprite.spritecollideany(pipetop, mario_group):
        controls = False
        mario.rect.centerx = pipe.rect.centerx
        mario.rect.top += 1
        if mario.rect.center[1] > height-110:
            mario.rect.center = 100, 0
    else: controls = True

def fireball_movement(fireball, width, height, speed, platfgroup, mario_group):
    # fireball will be moved by speed=[1,1] in every iteration
    # move_ip([x,y]) changes the Rect-objects left-top coordinates by x and y
    fireball.rect.move_ip(speed)
    # fireball bounces from the edges of the display surface
    if fireball.rect.left < 0 or fireball.rect.right > width: # fireball is vertically outside the game
        speed[0] = -speed[0] # the x-direction of the speed will be converted
    if fireball.rect.top < 0 or fireball.rect.bottom > height: # fireball is horizontally outside the game
        speed[1] = -speed[1] # the y-direction of the speed will be converted
    
def fb_collision(fireball, platfgroup, mario_group, speed):
    if pygame.sprite.spritecollideany(fireball, platfgroup) or pygame.sprite.spritecollideany(fireball, mario_group):
        boom = pygame.mixer.Sound("boom.wav")
        boom.play()
        fireball.update()
        speed[0] = r.randint(-1,1)