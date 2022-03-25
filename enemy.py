





import math
import pygame
import random
from tools import Images, Groups, Time, screen, screen_size
from enemy_attacks import LRLanceBarrage, NormalBarrage, LRLanceWhipType1, LRLanceWhipType2, LanceThrower, GenerateThrowers, TeleportBarrage

pygame.init()

class CrimsonAda(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, max_hp, health_bar_width, width, height, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.health_bar_width = health_bar_width
        self.heal_bar_ratio = self.max_hp/self.health_bar_width
        self.width = width
        self.height = height
        self.speed = speed
        self.alive = True
        self.sprite = Images.load_image('cute_thing2.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.ogimage = pygame.Surface([self.width, self.height], pygame.SRCALPHA).convert()
        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.image = self.ogimage
        self.rect = self.image.get_rect()        
        self.heartposx, self.heartposy = Groups.player_groups_dict['player_heart'].sprites()[0].rect.center

        self.attacks_list = ['Test']
        self.enemy_out_of_screen = True
        self.invencible = True
        

    def create_lr_lances(self):
        return LRLances(25, 25, screen_size)

    def normal_barrage(self):
        self.heartposx, self.heartposy = Groups.player_groups_dict['player_heart'].sprites()[0].rect.center
        if self.active_normal_barrage == True:
            if Time.current_time/1000 - self.first_normal_attack > self.normal_attack_duration:
                self.active_normal_barrage = False
                return
            if Time.current_time/1000 - self.normal_attack_start > self.normal_attack_cooldown:
                if self.normal_attack_cooldown > .1:
                    self.normal_attack_cooldown -= .05
                self.first_normal_attack = Time.current_time/1000
                self.normal_attack_start = Time.current_time/1000
                NormalBarrage(self.x, self.y, 5, 4, self.heartposx, self.heartposy, screen_size).generate_barrage()

    def choose_attack(self):
        if self.enemy_out_of_screen:
            return
        if Time.current_time/1000 - self.pattern_start > self.pattern_cooldown:
            self.pattern_start = Time.current_time/1000
            choice = random.choice(self.attacks_list)
            if choice == 'LanceBarrage':
                LRLanceBarrage(20, self.heartposx, self.heartposy, screen_size)
            elif choice == 'NormalBarrage':
                NormalBarrage(self.x, self.y, 5, 4, screen_size).generate_barrage()
            elif choice == 'LanceWhipType1':
                LRLanceWhipType1(20, self.heartposx, self.heartposy, screen_size)
            elif choice == 'LanceWhipType2':
                LRLanceWhipType2(20, self.heartposx, self.heartposy, screen_size)
            elif choice == 'FastXPattern':
                vx = 10
                vy = vx/100
                amount = 10
                LRLanceWhipType1('lr', amount, vx, vy, 1, self.heartposx, self.heartposy, screen_size)
                LRLanceWhipType2('lr', amount, vx, vy, 1, self.heartposx, self.heartposy, screen_size)
                LRLanceWhipType1('rl', amount, vx, vy, 1, self.heartposx, self.heartposy, screen_size)
                LRLanceWhipType2('rl', amount, vx, vy, 1, self.heartposx, self.heartposy, screen_size)

            elif choice == 'SlowXPattern':
                vx = .5
                vy = 0
                amount = 10
                increase = 1
                size = (10, 10)
                LRLanceWhipType1(amount, vx, vy, increase, size, self.heartposx, self.heartposy, screen_size)
                LRLanceWhipType2(amount, vx, vy, increase, size, self.heartposx, self.heartposy, screen_size)

            elif choice == 'ThrowerType2':
                self.static_pattern = True
                if self.first_thrower == 0:
                    self.first_thrower = Time.current_time/1000
                speed = .45
                width = 70
                height = 30

                GenerateThrowers(self.x, self.y, speed, width, height, self.width, self.height, ['up', 'down'], 'top', screen_size)
                if Time.current_time/1000 - self.first_thrower >= 1:
                    self.active_normal_barrage = True

            elif choice == 'ThrowerType2Teleport':
                tp_cooldown = 2.5
                if self.health_percent(25) <= self.hp <= self.health_percent(75):
                    tp_cooldown = 2

                if 0 <= self.hp <= self.health_percent(50):
                    tp_cooldown = 1.5

                if 0 <= self.hp <= self.health_percent(25):
                    tp_cooldown = 1

                print(tp_cooldown)

                print(f"HEALTH = {self.hp}   |   PERCENT = {self.health_percent(25)}")
                teleport = TeleportBarrage(self.heartposx, self.heartposy, tp_cooldown, self.tp_start, screen_size)
                teleport.tp()


                self.static_pattern = True
                if self.first_thrower == 0:
                    self.first_thrower = Time.current_time/1000
                speed = .45
                width = 35
                height = 35
                GenerateThrowers(self.x, self.y, speed, width, height, ['up', 'down'], 'top', screen_size)
                if Time.current_time/1000 - self.first_thrower >= 5:
                    self.active_normal_barrage = True

            elif choice == 'out_of_boundaries_waves':
                LRLanceBarrage(20, self.heartposx, self.heartposy, screen_size)
                pass

            elif choice == 'TeleportBarrage':
                tp_cooldown = 2.5
                if self.health_percent(25) <= self.hp <= self.health_percent(75):
                    tp_cooldown = .1

                if 0 <= self.hp <= self.health_percent(50):
                    tp_cooldown = 1.5

                if 0 <= self.hp <= self.health_percent(25):
                    tp_cooldown = 1

                teleport = TeleportBarrage(self.heartposx, self.heartposy, tp_cooldown, self.tp_start, screen_size)
                teleport.gen_barrage()

            elif choice == 'Test':
                pass

                pass
    def health_percent(self, percent):
        return self.max_hp*percent/100

    def update(self):
        self.angle = math.atan2(self.heartposy-self.y, self.heartposx-self.x)
        self.image = pygame.transform.rotate(self.ogimage, -math.degrees(self.angle)-90)
        self.rect = self.image.get_rect()
        if self.hp <= 0:
            self.alive = False
            self.kill()
        self.heartposx, self.heartposy = Groups.player_groups_dict['player_heart'].sprites()[0].rect.center
        self.rect.center = (int(self.x), int(self.y))

