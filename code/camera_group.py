from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = vector()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        
        self.line_start = vector(1, 1)
        self.path = []

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player, path_find):

        self.center_target_camera(player)
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset  # Apply camera offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        # self.path = path_find.a_star(self.line_start - self.offset, player.rect.center - self.offset)
        # self.path = path_find.a_star(self.line_start - self.offset, vector(600, 600) - self.offset)
        self.path = path_find.a_star(vector(1, 1), vector(9, 1))
        print(f"PATH: {self.path}")
        for i in range(len(self.path)):
            if i != len(self.path) - 1:
                pygame.draw.line(self.display_surface, (124,252,0), vector(self.path[i]) * TILE_SIZE + vector(32, 32) - self.offset, vector(self.path[i + 1]) * TILE_SIZE + vector(32, 32) - self.offset, 3)
