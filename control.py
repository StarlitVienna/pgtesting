




import os
import tools
import player
import pygame
from enemy import CrimsonAda
from tools import Groups, Time, Images, GetEvent
from functools import partial
from player_weapon import MainWeapon, Bomb
from mainmenu import menu

pygame.init()
pygame.font.init()

class Control:
    def __init__(self, fullscreen, diff, screen_size, screen):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.bg_color = (25, 25, 25)
        self.screen = screen
        self.screen_size = screen_size
        self.screen_rect = self.screen.get_rect()

    def run(self):
        while self.running:
            GetEvent.event = pygame.event.get()
            for event in GetEvent.event:
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            dt = self.clock.tick(self.fps)
            Time.dt = dt
            Time.slow_dt = dt/5
            Time.current_time = pygame.time.get_ticks()
            Time.current_fps = self.clock.get_fps()
                   
    def update(self):
        self.screen.fill(self.bg_color)
        menu.update_screen()
        pygame.display.flip()

