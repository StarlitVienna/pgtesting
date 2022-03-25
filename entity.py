





import pygame
from functools import partial
from tools import Groups, Images, screen, screen_size
from player import Character
from enemy import CrimsonAda
from enemyattackmain import bullet_gen
import cProfile

pygame.init()


class Entities:
    def __init__(self):
        self.player = Character(screen_size[0]/2, screen_size[1]-75, 50, 50, None)
        self.enemy = CrimsonAda(screen_size[0]/2, -63, 1000, 1000, screen_size[0]/2, 66, 63, None)

        Groups.add_to_player_group('player', self.player)
        Groups.add_to_enemy_group('enemy', self.enemy)

        self.player_dict = {
            'player_movement': self.player.movement,
            'player_update': self.player.update,
            'player_cursor_update': Groups.player_groups_dict['player_cursor'].update,
            'player_bullet_update': Groups.player_groups_dict['player_bullets'].update,
            'player_bomb_update': Groups.player_groups_dict['player_bombs'].update,
            'player_bomb_explosion_update': Groups.player_groups_dict['player_bomb_explosion'].update,
            'player_bomb_cooldown_update': self.player.update_bomb_cooldown,
            'player_heart_draw': partial(Groups.player_groups_dict['player_heart'].draw, screen),
            'player_bomb_draw': partial(Groups.player_groups_dict['player_bombs'].draw, screen),
            'player_bomb_explosion_draw': partial(Groups.player_groups_dict['player_bomb_explosion'].draw, screen),
            'player_bullet_draw': partial(Groups.player_groups_dict['player_bullets'].draw, screen),
            'player_cursor_draw': partial(Groups.player_groups_dict['player_cursor'].draw, screen),
            'player_draw': partial(Groups.player_groups_dict['player'].draw, screen),
            }

        self.enemy_dict = {
            'enemy_pattern_attack': bullet_gen.update,
            'enemy_update': self.enemy.update,
            'enemy_attack_update': Groups.enemy_groups_dict['enemy_lances'].update,
            'enemy_attack_draw': partial(Groups.enemy_groups_dict['enemy_lances'].draw, screen),
            'enemy_draw': partial(Groups.enemy_groups_dict['enemy'].draw, screen),
            }

entities = Entities()

def update_entities():
    if entities.enemy.alive:
        for x in entities.enemy_dict:
            entities.enemy_dict[x]()
    else:
        for group_name in Groups.enemy_groups_dict:
            Groups.enemy_groups_dict[group_name].empty()
    if entities.player.alive:
        for i in entities.player_dict:
            entities.player_dict[i]()

def update_main_menu():
    Groups.menu_groups_dict['box_sprite'].update()
    Groups.menu_groups_dict['box_sprite'].draw(screen)
    Groups.menu_groups_dict['cursor'].update()
        




