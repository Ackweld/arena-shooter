from settings import *
from sprites import Sprite
from player import Player
from camera_group import CameraGroup


class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.ground_rect = self.display_surface.get_frect(topleft=(0, 0))

        # groups
        # self.all_sprites = pygame.sprite.Group()
        self.camera_group = CameraGroup()
        self.colllision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):

        for x, y, surf in tmx_map.get_layer_by_name('Floor').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
                   self.camera_group)
        for x, y, surf in tmx_map.get_layer_by_name('Walls').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
                   (self.camera_group, self.colllision_sprites))
        for x, y, surf in tmx_map.get_layer_by_name('Yellow').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
                   self.camera_group)
        for x, y, surf in tmx_map.get_layer_by_name('Blue_Glow').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf,
                   self.camera_group)
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                # Player size is 128 px. Get rect center by taking top left + player size / 4
                self.player = Player((obj.x + obj.width / 4, obj.y + obj.height / 4), self.camera_group,
                                     self.colllision_sprites)
                print('PLAYER POS: ', obj.x, obj.y)

    def run(self, dt):
        self.camera_group.update(dt)
        self.display_surface.fill('black')
        self.camera_group.custom_draw(self.player)
