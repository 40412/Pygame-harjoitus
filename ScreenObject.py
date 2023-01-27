import pygame, sys
import random as r
from math import *

class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface((width,height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.top = pos_y

class Mario(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 250
        self.health = 6
        self.isalive = True

    def update(self):
        self.health -= 1
        if self.health == 1:
            self.image.set_alpha(50)
        if self.health == 0:
            self.isalive = False

    def reset(self):
        self.health = 6
        self.isalive = True
        self.rect.center = 100, 250
        self.image.set_alpha(255)

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, picture_path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = x_pos, y_pos
        self.random_movement_speed = 1
        self.random_reset_pos = r.randint(1000, 2000)

    def update(self):
        self.image.set_alpha(0)
        self.rect.center = (r.randint(100,800), 50)
        self.image.set_alpha(255)

    def koopa_move(self):
        self.rect.centerx += self.random_movement_speed
        if self.rect.centerx > self.random_reset_pos:
            self.rect.centerx = 0
            self.random_movement_speed = r.randint(1,2)
            self.random_reset_pos = r.randint(1200, 2500)
            self.rect.centery = r.randint(150, 400)

    def spiny_move(self, x):
        self.rect.centerx += r.randint(0,1)
        if self.rect.centerx > self.random_reset_pos:
            self.random_reset_pos = r.randint(1200, 2500)
            self.rect.centerx = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, picture_path):
        super().__init__()
        self.residual = False # True if bullet should die
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = (self.x, self.y)
        self.angle = angle
        self.speed = 2

    def update(self):
        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed
        self.rect.center = (self.x, self.y)
        if self.x > 960 or self.x < 0:
            self.residual = True
        if self.y > 600 or self.y < 0:
            self.residual = True

    def draw_bullet(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (240,0,0), pygame.Rect(self.x, self.y, 10, 10))