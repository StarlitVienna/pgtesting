





import pygame
from add_player import player_character


pygame.init()

class GetKeys:

    keys = pygame.key.get_pressed()


    w = keys[pygame.K_w]
    a = keys[pygame.K_a]
    s = keys[pygame.K_s]
    d = keys[pygame.K_d]

    ctrl = keys[pygame.K_LCTRL]
    space = keys[pygame.K_SPACE]

    def detect_key(self):
        if w:
            player_character.y -= player_character.speed
        if s:
            player_character.y += player_character.speed
        if a:
            player_character.x -= player_character.speed
        if d:
            player_character.x += player_character.speed
            
