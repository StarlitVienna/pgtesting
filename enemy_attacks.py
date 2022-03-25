





import math
from scipy import constants
import pygame
import random
from tools import Images, Time, Groups

pygame.init()


class LRLanceBarrageLances(pygame.sprite.Sprite):
    def __init__(self, xdirection, x, y, direction, xv, yv, size, heartx, hearty, following, screen_size):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.xdirection = xdirection
        self.yv = yv
        self.xv = xv
        self.size = size
        self.screen_size = screen_size
        self.width, self.height = size
        self.following = following

        self.amount = random.randint(10, 50)
        self.sprite = Images.load_image('bullet_test_enemy.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.image = pygame.Surface([self.width, self.height]).convert()
        self.rect = self.image.get_rect()
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))
        self.angle = math.atan2(hearty-self.y, heartx-self.x)


    def update(self):
        

        if self.following:
            self.dx = math.cos(self.angle)*Time.get_dt()/2
            self.dy = math.sin(self.angle)*Time.get_dt()/2
            self.x += self.dx
            self.y += self.dy
            self.rect.center = (int(self.x), int(self.y))
        else:
            if self.direction == 'up':
                self.y -= self.yv
            elif self.direction == 'down':
                self.y += self.yv
            if self.xdirection == 'lr':
                self.x += self.xv
            elif self.xdirection == 'rl':
                self.x -= self.xv

            self.rect.center = (self.x, self.y)

        if self.x <= 0 or self.x > self.screen_size[0] or self.y <= 0 or self.y >= self.screen_size[1]:
            self.kill()
        pass

class LRLanceBarrage:
    def __init__(self, amount, heartx, hearty, screen_size):
        lances_gap = int(screen_size[1]/amount)
        for gap in range(lances_gap, screen_size[1], lances_gap):
            x_base_speed = 12
            y_base_speed = 1
            for distance in range(int(abs(gap-hearty))):
                y_base_speed += 0.01
            for distance in range(int(abs(heartx))):
                x_base_speed += 0.005
            if hearty < gap:
                direction = 'up'
            elif hearty > gap:
                direction = 'down'
            else:
                direction = None
            lance_barrage = LRLanceBarrageLances('rl', screen_size[0], gap-5, direction, x_base_speed, y_base_speed, (10, 10), heartx, hearty, True, screen_size)
            Groups.add_to_enemy_group('enemy_lances', lance_barrage)


class LRLanceWhipType1:
    def __init__(self, amount, x_base_speed, y_base_speed, increase, size, player_x_pos, player_y_pos, screen_size):
        lances_gap = int(screen_size[1]/amount)
        xdirections = ['rl', 'lr']
        for xdirection in xdirections:
            self.xv = x_base_speed
            for gap in range(lances_gap, screen_size[1], lances_gap):
                self.xv += increase
                if player_y_pos < gap:
                    direction = 'up'
                elif player_y_pos > gap:
                    direction = 'down'
                else:
                    direction = None

                if xdirection == 'lr':
                    barrage_x = 0
                else:
                    barrage_x = screen_size[0]

                lance_barrage = LRLanceBarrageLances(xdirection, barrage_x, gap-5, direction, self.xv, y_base_speed, size, screen_size)
                Groups.add_to_enemy_group('enemy_lances', lance_barrage)



class LRLanceWhipType2:
    def __init__(self, amount, x_base_speed, y_base_speed, increase, size, player_x_pos, player_y_pos, screen_size):
        lances_gap = int(screen_size[1]/amount)
        xdirections = ['lr', 'rl']
        for xdirection in xdirections:
            self.xv = x_base_speed
            for gap in reversed(range(lances_gap, screen_size[1], lances_gap)):
                self.xv += increase

                if player_y_pos < gap:
                    direction = 'up'
                elif player_y_pos > gap:
                    direction = 'down'
                else:
                    direction = None
                
                if xdirection == 'lr':
                    barrage_x = 0
                else:
                    barrage_x = screen_size[0]

                lance_barrage = LRLanceBarrageLances(xdirection, barrage_x, gap-5, direction, self.xv, y_base_speed, size, screen_size)
                Groups.add_to_enemy_group('enemy_lances', lance_barrage)


class LanceThrowerLances(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, width, height, screen_size):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.direction = direction
        self.screen_size = screen_size
        self.damage = 1

        self.sprite = Images.load_image(f'bullet_test_enemy_down.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.image = pygame.Surface([self.width, self.height]).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))


    def update(self):
        if self.direction == 'right':
            self.x -= self.speed*Time.dt
        elif self.direction == 'left':
            self.x += self.speed*Time.dt
        elif self.direction == 'up':
            self.y -= self.speed*Time.dt
        elif self.direction == 'down':
            self.y += self.speed*Time.dt

        self.rect.center = (self.x, self.y)
        if self.y >= self.screen_size[1] or self.y <= 0 or self.x <= 0 or self.x >= self.screen_size[0]:
            self.kill()
        pass


class LanceThrower(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, width, height, directions, thrower_direction, screen_size):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.thrower_direction = thrower_direction
        self.screen_size = screen_size
        self.damage = 2
        self.enemy = Groups.enemy_groups_dict['enemy'].sprites()[0]
        
        self.directions = directions

        self.sprite = Images.load_image(f'bullet_test_enemy_{thrower_direction}.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.image = pygame.Surface([self.width, self.height]).convert()
        self.rect = self.image.get_rect()
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))
        
        self.throw_start = 0
        self.throw_cooldown_min = .1
        self.throw_cooldown_max = 1
        if  self.enemy.max_hp / self.enemy.hp >= 2 and self.enemy.max_hp / self.enemy.hp < 4:
            self.throw_cooldown_max = .5
        elif self.enemy.max_hp / self.enemy.hp >= 3:
            self.throw_cooldown_max = .1
        self.throw_cooldown = random.uniform(self.throw_cooldown_min, self.throw_cooldown_max)



    def update(self):
        if self.thrower_direction == 'left':
            self.x -= self.speed*Time.get_dt()
        elif self.thrower_direction == 'right':
            self.x += self.speed*Time.get_dt()
        else:
            self.y += self.speed*Time.get_dt()
        if Time.current_time/1000 - self.throw_start > self.throw_cooldown:
            self.throw_start = pygame.time.get_ticks()/1000
            for direction in self.directions:
                if direction == 'down' or direction == 'up':
                    width = 15
                    height = 35

                elif direction == 'left' or direction == 'right':
                    width = 35
                    height = 15
                
                if direction == 'down':
                    Groups.add_to_enemy_group('enemy_lances', LanceThrowerLances(self.x, self.y+self.height, self.speed/2, direction, width, height, self.screen_size))
                elif direction == 'up':
                    Groups.add_to_enemy_group('enemy_lances', LanceThrowerLances(self.x, self.y-self.height, self.speed/2, direction, width, height, self.screen_size))


        self.rect.center = (self.x, self.y)
        if self.y >= self.screen_size[1] or self.y <= 0 or self.x <= 0 or self.x >= self.screen_size[0]:
            self.kill()
        pass


class GenerateThrowers:
    def __init__(self, x, y, speed, width, height, enemy_width, enemy_height, directions, thrower_type, screen_size):

        if thrower_type == 'top':
            thrower_directions = ['left', 'right']
            for thrower_direction in thrower_directions:
                if thrower_direction == 'left':
                    Groups.add_to_enemy_group('enemy_lances', LanceThrower(x-enemy_width/2, y, speed, width, height, directions, thrower_direction, screen_size))
                else:
                    Groups.add_to_enemy_group('enemy_lances', LanceThrower(x+enemy_width/2, y, speed, width, height, directions, thrower_direction, screen_size))

        else:
            Groups.add_to_enemy_group('enemy_lances', LanceThrower(self.x, self.y, speed, width, height, self.directions, None, self.screen_size))


class NormalBarrageLances(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, width, height, targetx, targety, screen_size):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height

        self.sprite = Images.load_image('bullet_test_enemy_up.png')
        self.sprite = Images.scale(self.sprite, (self.width, self.height))
        self.ogimage = pygame.Surface([self.width, self.height]).convert()
        self.rect = self.ogimage.get_rect()
        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.angle = math.atan2(targety-self.y, targetx-self.x)
        self.image = pygame.transform.rotate(self.ogimage, -math.degrees(self.angle))
        self.damage = 1


    def update(self):
        self.dx = math.cos(self.angle)*Time.get_dt()/2
        self.dy = math.sin(self.angle)*Time.get_dt()/2
        self.x += self.dx
        self.y += self.dy
        self.rect = self.image.get_rect()


        self.rect.center = (int(self.x), int(self.y))
        pass


class NormalBarrage:
    def __init__(self, x, y, amount, speed, targetx, targety, screen_size):
        self.x = x
        self.y = y
        self.amount = amount
        self.speed = speed
        self.targetx = targetx
        self.targety = targety
        self.screen_size = screen_size
        self.barrage_cooldown = 1
        self.barrage_start = 0
    
    def generate_barrage(self):
        self.barrage_start = pygame.time.get_ticks()/1000
        Groups.add_to_enemy_group('enemy_lances', self.generate_lances())
    
    def generate_lances(self):
        return NormalBarrageLances(self.x, self.y, self.speed, 35, 15, self.targetx, self.targety, self.screen_size)

        pass

class TPLances(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.sprite = Images.load_image('square.png')
        self.sprite = Images.scale(self.sprite, (width, height))
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))
        self.damage = 1
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)

class TPLancesTest(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction, heartx, hearty, screen_size, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.enemy = Groups.enemy_groups_dict['enemy'].sprites()[0]
        self.heartx = heartx
        self.hearty = hearty
        self.screen_size = screen_size
        self.ogimage = pygame.Surface([width, height])
        self.ogsprite = Images.load_image('bullet_test_enemy_up.png')
        self.sprite = Images.scale(self.ogsprite, (width, height))
        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.damage = 1
        self.degrees = 0
        self.angle = angle
        self.start_angle = angle
        self.image = pygame.transform.rotate(self.ogimage, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.vel_x = 0
        self.vel_y = 0
        
        self.start = Time.current_time
        self.cooldown = 5
        self.complete = False
        self.starter = False


    def calculate_new_xy(self, old_xy, speed, angle_in_radians):
        new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
        new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
        return (new_x, new_y)

    def calc_vel(self, xy, speed, angle):
        self.vel_x = speed * math.cos(math.radians(angle))
        self.vel_y = speed * math.sin(math.radians(angle))

       
    def update(self):
        
        if self.rect.centerx <= 0 or self.rect.centerx >= self.screen_size[0] or self.rect.centery <= 0 or self.rect.centery >= self.screen_size[1]:
            self.kill()

        self.angle += 1


        if self.angle >= 360:
            self.angle = 0

        self.image = pygame.transform.rotate(self.ogimage, -self.angle)
        self.rect = self.image.get_rect()
        self.calc_vel(self.rect.center, Time.dt/2, self.angle)
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)



class TeleportBarrage:
    def __init__(self, heartx, hearty, cooldown, tp_start, screen_size):
        self.heartx = heartx
        self.hearty = hearty
        self.cooldown = cooldown
        self.screen_size = screen_size
        self.enemy = Groups.enemy_groups_dict['enemy'].sprites()[0]

        self.tp_start = tp_start
        self.tpx = 0
        self.tpy = 0

    
    def calc_tp(self):
        self.tpx = random.randint(self.enemy.width, self.screen_size[0]-self.enemy.width)
        self.tpy = random.randint(self.enemy.height, self.screen_size[1]-self.enemy.height)
        
        if self.heartx-100 <= self.tpx <= self.heartx+100 or self.hearty-100 <= self.tpy <= self.hearty+100:
            return self.calc_tp()

    def gen_barrage(self):
        amount = 10
        for i in range(0, 360, amount):


            lances = TPLancesTest(self.enemy.x, self.enemy.y, 28, 12, None, self.enemy.x, self.enemy.y, self.screen_size, i)

            Groups.add_to_enemy_group('enemy_lances', lances)



    def tp(self):
        if Time.current_time/1000 - self.tp_start >= self.cooldown:
            self.enemy.tp_start = Time.current_time/1000
            self.calc_tp()
            self.enemy.x = self.tpx
            self.enemy.y = self.tpy
            self.angle = math.atan2(self.hearty-self.enemy.y, self.heartx-self.enemy.x)
            self.enemy.image = pygame.transform.rotate(self.enemy.ogimage, -math.degrees(self.angle)-90)
            self.enemy.rect = self.enemy.image.get_rect()


