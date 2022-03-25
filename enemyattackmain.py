





import math
import random
import numpy
import pygame
from tools import Images, Groups, Time, screen_size


pygame.init()


class AngledStopBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, width, height, angle):
        super().__init__()

        self.x = x
        self.y = y
        self.ogsprite = Images.load_image(sprite)
        self.sprite = Images.scale(self.ogsprite, (width, height))
        self.width = width
        self.height = height
        self.angle = angle
        self.ogimage = pygame.Surface([width, height])
        self.ogimage.blit(self.sprite, (0,0))
        self.ogimage.set_colorkey((0,0,0))
        self.image = pygame.transform.rotate(self.ogimage, -angle)
        self.rect = self.image.get_rect()
        self.damage = 1
        self.dx_x = 0
        self.dx_y = 0

        self.delay = 2
        self.start = Time.current_time/1000
        self.decrease_angle = 1

    def calc_dx(self, xy, speed, angle):
        self.dx_x = speed * math.cos(math.radians(angle))
        self.dx_y = speed * math.sin(math.radians(angle))

    def update(self):
        if Time.current_time/1000 - self.start >= self.delay:
            self.calc_dx((self.x, self.y), Time.dt/2, self.angle)
            self.angle -= self.decrease_angle
            if self.decrease_angle <= 0:
                self.decrease_angle = 0
            else:
                self.decrease_angle -= .001


        self.image = pygame.transform.rotate(self.ogimage, -self.angle)

        self.rect = self.image.get_rect()
        self.x += self.dx_x
        self.y += self.dx_y
        self.rect.center = (self.x, self.y)

        if self.x <= 0 or self.x >= screen_size[0] or self.y >= screen_size[1] or self.y <=0:
            self.kill()


scaled_sprite = Images.scale(Images.load_image('enemy_main.png'), (25, 25))
bullet_surface = pygame.Surface([25, 25]).convert()
bullet_surface.set_colorkey((0,0,0))
bullet_surface.blit(scaled_sprite, (0,0))
class AngledBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, width, height, angle):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.damage = 1
        self.dx_x = 0
        self.dx_y = 0
        e = 2.718281828459045
        pi = 3.141592653589793
        self.angle_cos = (e**(angle*pi/180*1j)).real
        self.angle_sin = (e**(angle*pi/180*1j)).imag

    def calc_dx(self, xy, speed, angle):
        self.dx_x = speed * numpy.cos(numpy.radians(angle))
        self.dx_y = speed * numpy.sin(numpy.radians(angle))

    def update(self):
        self.x += self.angle_cos*Time.dt/5
        self.y += self.angle_sin*Time.dt/5
        self.rect.center = (self.x, self.y)

        if self.x <= 0 or self.x >= screen_size[0] or self.y >= screen_size[1] or self.y <=0:
            self.kill()
            pass


class GenBullets:
    def __init__(self):
        self.active_patterns = {
                'all_sides': False,
                'teleport': False,
                'all_sides_tp': False,
                'barrage': False,
                'delayed_barrage': False,
                'delayed_sides_barrage': False,
                'spirals': False,
                'standard_spiral': False,
                'shotg': False,
                }
        self.patterns_cooldown = {
                'all_sides': .1,
                'teleport': .25,
                'all_sides_tp': .5,
                'barrage': .1,
                'delayed_barrage': .25,
                'delayed_sides_barrage': .5,
                'spirals': .025,
                'standard_spiral': .01,
                'shotg': .01,
                }
        self.patterns_start = {
                'all_sides': 0,
                'teleport': 0,
                'all_sides_tp': 0,
                'barrage': 0,
                'delayed_barrage': 0,
                'delayed_sides_barrage': 0,
                'spirals': 0,
                'standard_spiral': 0,
                'shotg': 0,
                }
        self.patterns_first_start = {
                'all_sides': 0,
                'teleport': 0,
                'all_sides_tp': 0,
                'barrage': 0,
                'delayed_barrage': 0,
                'delayed_sides_barrage': 0,
                'spirals': 0,
                'standard_spiral': 0,
                'shotg': 0,
                }
        self.patterns_duration = {
                'all_sides': 5,
                'teleport': 5,
                'all_sides_tp': 10,
                'barrage': 10,
                'delayed_barrage': 10,
                'delayed_sides_barrage': 10,
                'spirals': 10000000,
                'standard_spiral': 10,
                'shotg': 10,
                }
        
        self.first_appearance = True
        self.out_of_screen = True
        self.made_first_choice = False
        self.enemy = None
        self.player = None
        self.spiral_angle = 1


    def get_into_screen(self):
        if self.enemy.y < 63:
            self.enemy.y += screen_size[1]/100
        else:
            self.out_of_screen = False

    def get_out_of_screen(self):
        if self.enemy.y > -63:
            self.enemy.y -= screen_size[1]/100

    def first_choice(self):
        patterns = ['spirals']
        pattern = random.choice(patterns)
        self.active_patterns[pattern] = True
    
    def move_to_middle(self):
        angle = math.atan2(screen_size[1]/2-self.enemy.y, screen_size[0]/2-self.enemy.x)
        dx = math.cos(angle)*Time.dt
        dy = math.sin(angle)*Time.dt

        if self.enemy.y > screen_size[1]/2:
            self.enemy.y += dy
            if self.enemy.y + dy < screen_size[1]/2:
                self.enemy.y = screen_size[1]/2

        if self.enemy.y < screen_size[1]/2:
            self.enemy.y += dy
            if self.enemy.y + dy >= screen_size[1]/2:
                self.enemy.y = screen_size[1]/2

        if self.enemy.x > screen_size[0]/2:
            self.enemy.x += dx
            if self.enemy.x + dx <= screen_size[0]/2:
                self.enemy.x = screen_size[0]/2

        if self.enemy.x < screen_size[0]/2:
            self.enemy.x += dx
            if self.enemy.x + dx >= screen_size[0]/2:
                self.enemy.x = screen_size[0]/2


    
    def check_cooldown(self, pattern):
        if self.patterns_first_start[pattern] == 0:
            self.patterns_first_start[pattern] = Time.current_time/1000
        if Time.current_time/1000 - self.patterns_first_start[pattern] >= self.patterns_duration[pattern]:
            self.active_patterns[pattern] = False
            self.patterns_first_start[pattern] = 0
            return


    def cooldown_restart(self, pattern):
        self.patterns_first_start[pattern] = 0



    def all_sides(self):
        self.check_cooldown('all_sides')
        for angle in range(0, 360, 20):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))

    def calc_tp(self):
        self.enemy.x = numpy.random.randint(self.enemy.width, screen_size[0]-self.enemy.width)
        self.enemy.y = numpy.random.randint(self.enemy.height, screen_size[1]-self.enemy.height)

        if self.player.x-150 <= self.enemy.x <= self.player.x+150 or self.player.y-150 <= self.enemy.y <= self.player.y+150:
            self.calc_tp()

    def teleport(self):
        self.check_cooldown('teleport')
        self.calc_tp()

    def all_sides_tp(self):
        self.calc_tp()
        self.check_cooldown('all_sides_tp')
        for angle in range(0, 360, 20):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))


    def delayed_sides_barrage(self):
        self.calc_tp()
        self.check_cooldown('all_sides_tp')
        for angle in range(0, 360, 20):
            Groups.add_to_enemy_group('enemy_lances', AngledStopBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))



    def barrage(self):
        player_angle = math.atan2(self.player.y-self.enemy.y, self.player.x-self.enemy.x)
        self.check_cooldown('barrage')
        print(self.angle_enemy_player())

        for angle in range(0, 190, 10):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))
            print(angle)

    def delayed_barrage(self):
        player_angle = math.atan2(self.player.y-self.enemy.y, self.player.x-self.enemy.x)
        print('timed')
        self.check_cooldown('barrage')
        print(self.angle_enemy_player())

        for angle in range(0, 190, 10):
            Groups.add_to_enemy_group('enemy_lances', AngledStopBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))
            print(angle)
    def standard_spiral(self):
        self.check_cooldown('standard_spiral')
        if self.spiral_angle >= 360:
            self.spiral_angle = 0
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 90):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        self.spiral_angle += 5
    
    def testspirals(self):
        pass

    def shotg(self):
        self.check_cooldown('shotg')
        if self.spiral_angle >= 360:
            self.spiral_angle = 1
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        for angle in range(0-self.spiral_angle, 360-self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        self.spiral_angle += 5


    def player_spiral(self):
        pass

    def spirals(self):
        self.check_cooldown('spirals')
        if self.spiral_angle >= 360:
            self.spiral_angle = 1
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        for angle in range(0-self.spiral_angle, 360-self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        self.spiral_angle += 5


    def quad_spirals(self):
        self.check_cooldown('quad_spirals')
        if self.spiral_angle >= 360:
            self.spiral_angle = 0
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 90):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        for angle in range(0-self.spiral_angle, 360-self.spiral_angle, 90):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        self.spiral_angle += 5

    def spread_spirals(self):
        self.check_cooldown('spread_spirals')
        if self.spiral_angle >= 360:
            self.spiral_angle = 0
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 20):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        for angle in range(0-self.spiral_angle, 360-self.spiral_angle, 20):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 15, 15, angle))
        self.spiral_angle += 5



   
    def spiral_flower(self):
        self.check_cooldown('spiral_flower')
        if self.spiral_angle >= 360:
            self.spiral_angle = 0
        for angle in range(0+self.spiral_angle, 360+self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))
        for angle in range(0-self.spiral_angle, 360-self.spiral_angle, 40):
            Groups.add_to_enemy_group('enemy_lances', AngledBullets(self.enemy.x, self.enemy.y, 'bullet_test_enemy_left.png', 35, 15, angle))
        self.spiral_angle += 5


    def angle_enemy_player(self):
        rads = math.atan2(-self.player.y-self.enemy.y, self.player.x-self.enemy.x)
        rads %= 2*math.pi
        return math.degrees(rads)

    def check_if_middle(self):
        if self.enemy.x == screen_size[0]/2 and self.enemy.y == screen_size[1]/2:
            return True
        else:
            return False


        


    def execute_patterns(self):

        if self.active_patterns['teleport'] and Time.current_time/1000 - self.patterns_start['teleport'] >= self.patterns_cooldown['teleport']:
            self.patterns_start['teleport'] = Time.current_time/1000
            self.teleport()

        if self.active_patterns['all_sides'] and Time.current_time/1000 - self.patterns_start['all_sides'] >= self.patterns_cooldown['all_sides']:
            self.patterns_start['all_sides'] = Time.current_time/1000
            self.all_sides()

        elif self.active_patterns['all_sides'] and not self.active_patterns['teleport'] and not self.active_patterns['all_sides_tp']:
            self.move_to_middle()

        if self.active_patterns['all_sides_tp'] and Time.current_time/1000 - self.patterns_start['all_sides_tp'] >= self.patterns_cooldown['all_sides_tp']:
            self.patterns_start['all_sides_tp'] = Time.current_time/1000
            self.all_sides_tp()
        
        if self.active_patterns['barrage'] and Time.current_time/1000 - self.patterns_start['barrage'] >= self.patterns_cooldown['barrage']:
            self.patterns_start['barrage'] = Time.current_time/1000
            self.barrage()

        if self.active_patterns['delayed_barrage'] and Time.current_time/1000 - self.patterns_start['delayed_barrage'] >= self.patterns_cooldown['delayed_barrage']:
            self.patterns_start['delayed_barrage'] = Time.current_time/1000
            self.delayed_barrage()
        
        if self.active_patterns['delayed_sides_barrage'] and Time.current_time/1000 - self.patterns_start['delayed_sides_barrage'] >= self.patterns_cooldown['delayed_sides_barrage']:
            self.patterns_start['delayed_sides_barrage'] = Time.current_time/1000
            self.delayed_sides_barrage()
       
        if self.active_patterns['spirals'] and not self.check_if_middle():
            self.move_to_middle()
        elif self.active_patterns['spirals'] and Time.current_time/1000 - self.patterns_start['spirals'] >= self.patterns_cooldown['spirals']:
            self.patterns_start['spirals'] = Time.current_time/1000
            self.spirals()
        
        if self.active_patterns['shotg'] and Time.current_time/1000 - self.patterns_start['shotg'] >= self.patterns_cooldown['shotg']:
            self.patterns_start['shotg'] = Time.current_time/1000
            self.shotg()





    def update(self):
        self.player = Groups.player_groups_dict['player'].sprites()[0]
        self.enemy = Groups.enemy_groups_dict['enemy'].sprites()[0]
        if self.first_appearance and self.enemy.y < 63:
            self.get_into_screen()
            return
        else:
            self.first_appearance = False
        if not self.made_first_choice:
            self.first_choice()
            self.made_first_choice = True

        self.execute_patterns()



bullet_gen = GenBullets()



