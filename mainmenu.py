





import pygame
from entity import update_entities, update_main_menu, entities
from tools import screen, screen_size, Images, Groups, GetEvent, Time

pygame.init()
screens_dict = {
        'main_menu': True,
        'gameplay': False,
        }

def start_game():
    screens_dict['main_menu'] = False
    screens_dict['gameplay'] = True


class SelectBox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, action):
        super().__init__()
        self.x = x
        self.y = y
        self.ogwidth = width
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.ogsprite = Images.load_image('box.png')
        self.sprite = Images.scale(self.ogsprite, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))
        self.action = action
    
    def update(self):
        self.image = pygame.Surface([self.width, self.height])
        self.sprite = Images.scale(self.ogsprite, (self.width, self.height))
        self.image.blit(self.sprite, (0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        collide = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.width <= self.ogwidth+68 and collide:
            self.width += 4
        elif self.width >= self.ogwidth and not collide:
            self.width -= 4
        for event in GetEvent.event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.action:
                        self.action()


        pass


class Menu:
    def __init__(self, font, color):
        self.font = font
        self.color = color
        self.current_option = -1
        self.gen_main_menu_sprites()
        pygame.mouse.set_visible(True)
    
    def draw_text(self, size, text, anti_alias, option_number, xy):
        text_font = pygame.font.SysFont(self.font, size)
        text_surface = text_font.render(text, anti_alias, self.color)
        text_rect = text_surface.get_rect()
        if xy:
            text_rect.center = xy
        else:
            text_rect.center = Groups.menu_groups_dict['box_sprite'].sprites()[option_number].rect.center
        screen.blit(text_surface, text_rect)

    def gen_main_menu_text(self):
        title_size = 200
        size = 40
        
        self.draw_text(title_size, 'Test', True, None, (screen_size[0]/2, 100))

        self.draw_text(size, 'New Game', True, 0, None)
        self.draw_text(size, 'Continue', True, 1, None)
        self.draw_text(size, 'Sandbox', True, 2, None)
        self.draw_text(size, 'Settings', True, 3, None)

    def gen_main_menu_sprites(self):
        padding = 102
        menu_actions = {
                0: None,
                1: None,
                2: None,
                }

            
        Groups.add_to_menu_group('box_sprite', SelectBox(screen_size[0]/2, screen_size[1]/2, 200, 68, start_game))
        for i in menu_actions:
            Groups.add_to_menu_group('box_sprite', SelectBox(screen_size[0]/2, screen_size[1]/2+padding, 200, 68, menu_actions[i]))
            padding += 102

    def select(self):
        keys = pygame.key.get_pressed()
        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        box_sprite = Groups.menu_groups_dict['box_sprite'].sprites()

    def update_game_objects(self):
        text_font = pygame.font.SysFont(self.font, 30)
        fps = text_font.render(f'FPS: {int(Time.current_fps)}', True, (255, 255, 255))
        hp = text_font.render(f'HP: {int(entities.player.heart.hp)}', True, (255, 255, 255))
        boss_hp = text_font.render(f'BOSS HEALTH: {int(entities.enemy.hp)}', True, (255, 255, 255))
        bullet_amount = text_font.render(f"BULLETS: {len(Groups.enemy_groups_dict['enemy_lances'])}", True, (255, 255, 255))
        screen.blit(fps, (0, screen_size[1]-30))
        screen.blit(hp, (0, screen_size[1]-60))
        screen.blit(boss_hp, (0, screen_size[1]-90))
        screen.blit(bullet_amount, (0, screen_size[1]-120))

    def update_screen(self):
        if screens_dict['main_menu']:
            self.gen_main_menu_text()
            self.select()
            update_main_menu()

        elif screens_dict['gameplay']:
            pygame.mouse.set_visible(False)
            self.update_game_objects()
            update_entities()
        else:
            pass

menu = Menu('Comic Sans MS', (255, 255, 255))
