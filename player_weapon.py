





import math
import pygame
import random
from tools import Images, Groups, Time

pygame.init()


class MainWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage, speed, fire_rate, screen_width, screen_height, targetx, targety):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.damage = damage
        self.fire_rate = fire_rate
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.angle = math.atan2(targety-self.y, targetx-self.x)

        self.ogimage = pygame.Surface([self.width, self.height])
        self.rect = self.ogimage.get_rect()

        self.sprite = Images.load_image('square.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))

        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.image = pygame.transform.rotate(self.ogimage, -math.degrees(self.angle))


    def update(self):
        self.dx = math.cos(self.angle)*Time.dt
        self.dy = math.sin(self.angle)*Time.dt
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))
        collisions = pygame.sprite.groupcollide(Groups.player_groups_dict['player_bullets'], Groups.enemy_groups_dict['enemy'], True, False)
        for collision in collisions:
            Groups.enemy_groups_dict['enemy'].sprites()[0].hp -= self.damage
            pass
        if self.y < 0 or self.x <= 0 or self.y >= self.screen_height or self.x >= self.screen_width:
            self.kill()
        pass

    def movement(self):
        pass


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage, speed, cooldown, cursorx, cursory, screen_width, screen_height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.cooldown = cooldown
        self.damage = damage
        self.number_of_fragments = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.explosion_radius = 500
        self.cursorx = cursorx
        self.cursory = cursory
        self.angle = math.atan2(self.cursory-self.y, self.cursorx-self.x)


        self.ogimage = pygame.Surface([self.width, self.height])
        self.rect = self.ogimage.get_rect()
        self.sprite = Images.load_image('square.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.image = pygame.transform.rotate(self.ogimage, -math.degrees(self.angle))

    def explode(self):
        Groups.add_to_player_group('player_bomb_explosion', self.create_explosion())
            
        pass

    def create_explosion(self):
        return NormalExplosion(self.x, self.y, 10, self.explosion_radius, self.width, self.height)


    def update(self):
        collisions = pygame.sprite.groupcollide(Groups.player_groups_dict['player_bombs'], Groups.enemy_groups_dict['enemy'], True, False)
        for collision in collisions:
            Groups.enemy_groups_dict['enemy'].sprites()[0].hp -= self.damage
            self.explode()
            pass
        
        self.dx = math.cos(self.angle)*Time.dt/2
        self.dy = math.sin(self.angle)*Time.dt/2

        self.x += self.dx
        self.y += self.dy

        self.rect.center = (int(self.x), int(self.y))
        if self.y < 0 or self.x <= 0 or self.x >= self.screen_width or self.y >= self.screen_height:
            self.kill()
            self.explode()


class NormalExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, radius, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.radius = radius
        self.width = width
        self.height = height

        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()

        self.sprite = Images.load_image('explosiontest.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))

        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))

        self.reached_max = False
        self.increase_amount = 0
        
        self.collision_start = 0
        self.collision_cooldown = .25

    def update(self):
        collisions = pygame.sprite.groupcollide(Groups.player_groups_dict['player_bomb_explosion'], Groups.enemy_groups_dict['enemy'], False, False)
        pygame.sprite.groupcollide(Groups.player_groups_dict['player_bomb_explosion'], Groups.enemy_groups_dict['enemy_lances'], False, True)
        for collision in collisions:
            if Time.current_time/1000 - self.collision_start >= self.collision_cooldown:
                self.collision_start = Time.current_time/1000
                Groups.enemy_groups_dict['enemy'].sprites()[0].hp -= self.damage

        if self.width < self.radius and not self.reached_max:
            self.increase_amount = Time.get_dt()
            self.width += self.increase_amount
            self.height += self.increase_amount
        elif self.width >= self.radius or self.reached_max == True:
            self.reached_max = True
            self.increase_amount = -Time.get_dt()/2
            self.width += self.increase_amount
            self.height += self.increase_amount
        if self.width <= 0:
            self.kill()

        else:
            self.sprite = Images.scale(Images.load_image('explosiontest.png'), (self.width, self.height))
            self.image = pygame.Surface([self.width, self.height])
            self.image.blit(self.sprite, (0,0))
            self.image.set_colorkey((0,0,0))
            self.rect = self.rect.inflate(self.increase_amount, self.increase_amount)
            self.rect.center = (self.x, self.y)
        pass


class NormalExplosionNoSurface:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = Images.load_image('square.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.rect = self.sprite.get_rect()

    def update(self):
        pass


class BombFragments(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.width = width
        self.height = height

        self.sprite = Images.load_image('player_main_weapon_bullets.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))

        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(self.sprite, (0, 0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

    def update(self):
        self.y += self.speed
        self.width += 10
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.rect.center = (self.x, self.y)
        pass


class Parry:
    def __init__(self, x, y, width, height, iseconds):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.iseconds = iseconds
        cooldown = .5
        start = 0
