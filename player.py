





import os
import math
import pygame
from tools import Groups, Images, Time, screen_size
from player_weapon import MainWeapon, Bomb, Parry, NormalExplosion
from player_heart import Heart
pygame.init()

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.alive = True

        self.heart = Heart(self.x, self.y, 5, 5, 100)
        Groups.add_to_player_group('player_heart', self.heart)

        self.cursor = Cursor(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 50, 50)
        Groups.add_to_player_group('player_cursor', self.cursor)

        self.ogimage = pygame.Surface([self.width, self.height]).convert()
        self.ogimage.set_colorkey((0,0,0))
        self.ogsprite = Images.load_image('nav.png')
        self.ogsprite = Images.scale(self.ogsprite, (self.width, self.height))

        self.ogimage.blit(self.ogsprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.rect = self.ogimage.get_rect()

        self.screen_width, self.screen_height = screen_size
       
        self.main_weapon_cooldown_start = 0
        self.main_weapon_cooldown = .05

        self.bomb_cooldown_start = 0
        self.bomb_cooldown = 5
        self.bomb_on_cooldown = False


        
        self.parry_iseconds = .05
        self.parry_start = 0
        self.parry_cooldown = .5

        self.invencible = False
    

    def movement(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]
        c = keys[pygame.K_c]
        p = keys[pygame.K_p]
        o = keys[pygame.K_o]
        

        left_click = mouse_keys[0]
        right_click = mouse_keys[2]

        ctrl = keys[pygame.K_LCTRL]
        lshift = keys[pygame.K_LSHIFT]
        rshift = keys[pygame.K_RSHIFT]
        space = keys[pygame.K_SPACE]

        if w and space:
            self.y -= int(Time.dt/4)
            if self.y <= self.height/2:
                self.y = self.height/2
        elif w:
            self.y -= int(Time.dt/2.5)
            if self.y <= self.height/2:
                self.y = self.height/2


        if s and space:
            self.y += int(Time.dt/4)
            if self.y >= self.screen_height-self.height/2:
                self.y = self.screen_height-self.height/2

        elif s:
            self.y += int(Time.dt/2.5)
            if self.y >= self.screen_height-self.height/2:
                self.y = self.screen_height-self.height/2

        
        if d and space:
            self.x += int(Time.dt/4)
            if self.x >= self.screen_width-self.width/2:
                self.x = self.screen_width-self.width/2

        elif d:
            self.x += int(Time.dt/2.5)
            if self.x >= self.screen_width-self.width/2:
                self.x = self.screen_width-self.width/2
        
        if a and space:
            self.x -= int(Time.dt/4)
            if self.x <= self.width/2:
                self.x = self.width/2

        elif a:
            self.x -= int(Time.dt/2.5)
            if self.x <= self.width/2:
                self.x = self.width/2


        if lshift or rshift:
            for bomb in Groups.player_groups_dict['player_bombs'].sprites():
                bomb.explode()


        if o:
            if Time.current_time/1000 - self.parry_start >= self.parry_cooldown:
                self.parry_start = pygame.time.get_ticks()/1000
                self.invencible = True

        if ctrl:
            for bomb in Groups.player_groups_dict['player_bombs'].sprites():
                bomb.explode()
            pass
    
        if left_click:
            if Time.current_time/1000 - self.main_weapon_cooldown >= self.main_weapon_cooldown_start:
                self.main_weapon_cooldown_start = Time.current_time/1000
                Groups.add_to_player_group('player_bullets', self.shoot())
        
        if c:
            if Time.current_time/1000 - self.bomb_cooldown >= self.bomb_cooldown_start:
                self.bomb_cooldown_start = Time.current_time/1000
                Groups.add_to_player_group('player_bombs', self.throw_bomb())
    
    def update_bomb_cooldown(self):
        if self.bomb_on_cooldown:
            if Time.current_time/1000 - self.bomb_cooldown_start > self.bomb_cooldown:
                self.bomb_on_cooldown = False

    def shoot(self):
        return MainWeapon(self.x, self.y, self.width/4, self.height/4, 1, Time.dt, 2, self.screen_width, self.screen_height, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def throw_bomb(self):
        return Bomb(self.x, self.y, self.width/2, self.height/2, 10, Time.dt/2, 10, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.screen_width ,self.screen_height)

    def create_player(self):
        return Character(100, 100, 50, 50)

    def update(self):
        if self.heart.hp <= 0:
            self.alive = False
            self.kill()
        targetx, targety = pygame.mouse.get_pos()
        self.angle = math.atan2(targety-self.y, targetx-self.x)
        self.image = pygame.transform.rotate(self.ogimage, -math.degrees(self.angle)).convert()
        self.rect = self.image.get_rect()


        self.rect.center = (self.x, self.y)
        self.heart.rect.center = (self.x, self.y)
        if self.invencible == True and Time.current_time/1000 - self.parry_start >= self.parry_iseconds:
            self.invencible = False
        collisions = pygame.sprite.spritecollide(self.heart, Groups.enemy_groups_dict['enemy_lances'], True)
        if self.invencible == False:
            for collision in collisions:
                self.heart.hp -= collision.damage
        else:
            if collisions:
                explosion = NormalExplosion(self.x, self.y, None, 100, 0, 0)
                Groups.add_to_player_group('player_bomb_explosion', explosion)

class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = Images.load_image('normalaim.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


