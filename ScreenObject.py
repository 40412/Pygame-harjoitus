import pygame
import random as r

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
        self.rect.center = (r.randint(100,800), 100)
        self.image.set_alpha(255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dest) -> None:
        super().__init__()
        self.image = pygame.Surface(5, 5)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.destination = dest
        