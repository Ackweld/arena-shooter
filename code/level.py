from settings import *
from sprites import Sprite
from player import Player
from enemy import Enemy
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

        for x, y, surf in tmx_map.get_layer_by_name("Floor").tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.camera_group
            )
        for x, y, surf in tmx_map.get_layer_by_name("Walls").tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surf,
                groups=(self.camera_group, self.colllision_sprites),
            )
        for x, y, surf in tmx_map.get_layer_by_name("Yellow").tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.camera_group
            )
        for x, y, surf in tmx_map.get_layer_by_name("Blue_Glow").tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surf, groups=self.camera_group
            )
        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "player":
                # Player size is 128 px. Get rect center by taking top left + player size / 2
                self.player = Player(
                    pos=(obj.x + obj.width / 2, obj.y + obj.height / 2),
                    groups=self.camera_group,
                    collision_sprites=self.colllision_sprites,
                )
                print("PLAYER POS: ", obj.x, obj.y)
        for obj in tmx_map.get_layer_by_name("Enemies"):
            if obj.name == "enemy":
                # Enemy size is 128 px. Get rect center by taking top left + enemy size / 2
                self.enemy = Enemy(
                    pos=(obj.x + obj.width / 2, obj.y + obj.height / 2),
                    groups=self.camera_group,
                    collision_sprites=self.colllision_sprites,
                    player=self.player,
                )
                print("ENEMY POS: ", obj.x, obj.y)

    def run(self, dt):
        self.camera_group.update(dt)
        self.display_surface.fill("black")
        self.camera_group.custom_draw(self.player)
