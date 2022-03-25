





import pygame
from tools import Groups

pygame.init()

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill((25, 25, 25))
        
