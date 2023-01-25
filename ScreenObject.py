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
        self.health = 3
        self.isalive = True

    def update(self):
        self.health -= 1
        if self.health == 1:
            self.image.set_alpha(50)
        if self.health == 0:
            self.isalive = False

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, picture_path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = x_pos, y_pos

    def update(self):
        self.image.set_alpha(0)
        self.rect.center = (r.randint(100,800), 50)
        self.image.set_alpha(255)

    def koopa_move(self):
        self.rect.centerx += 1
        if self.rect.centerx > 2500:
            self.rect.centerx = 0

    def spiny_move(self, x):
        pass

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, picture_path):
        super().__init__()
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

    def draw_bullet(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (240,0,0), pygame.Rect(self.x, self.y, 10, 10))