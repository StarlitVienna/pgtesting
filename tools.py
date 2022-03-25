






import os
import pygame

pygame.init()
flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
screen = pygame.display.set_mode((0,0), flags)
screen_size = screen.get_size()

class GetEvent:
    event = pygame.event.get()

class Images:
    sprites_path = './assets/sprites/'
    @staticmethod
    def load_image(file_name):
        image_path = f'{Images.sprites_path}/{file_name}'
        return pygame.image.load(os.path.abspath(image_path)).convert_alpha()

    def scale(sprite, size):
        return pygame.transform.scale(sprite, size)

class Time:
    dt = 0
    current_time = 0
    current_fps = 0
    slow_dt = 0
    def get_dt():
        return Time.dt

class Groups:
    
    menu_groups_dict = {
            'box_sprite': pygame.sprite.Group(),
            'cursor': pygame.sprite.Group(),
            }

    player_groups_dict = {
            'player': pygame.sprite.Group(),
            'player_heart': pygame.sprite.Group(),
            'player_cursor': pygame.sprite.Group(),
            'player_bullets': pygame.sprite.Group(),
            'player_bombs': pygame.sprite.Group(),
            'player_bomb_explosion': pygame.sprite.Group(),
            'player_bomb_fragments': pygame.sprite.Group(),
            }

    enemy_groups_dict = {
            'enemy': pygame.sprite.Group(),
            'enemy_lances': pygame.sprite.Group(),
            }

    def add_to_player_group(group, sprite):
        Groups.player_groups_dict[f'{group}'].add(sprite)
    def add_to_enemy_group(group, sprite):
        Groups.enemy_groups_dict[f'{group}'].add(sprite)
    def add_to_menu_group(group, sprite):
        Groups.menu_groups_dict[f'{group}'].add(sprite)

class States:
    def __init__(self):

        self.background = (25, 25, 25)

        self.quit = False
        self.text_color = (255, 255, 255)

        self.controls_dict = {
                'w': pygame.K_w,
                'a': pygame.K_a,
                's': pygame.K_s,
                'd': pygame.K_d,
                'escape': pygame.K_ESCAPE
                }
        

    def update_controller_dict(self, keyname, event):
            self.controls_dict[keyname] = event.key

