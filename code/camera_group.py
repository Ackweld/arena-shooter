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

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player, enemy):

        self.center_target_camera(player)

        enemy_path = enemy.get_path()

        points = []
        for point in enemy_path:
            points.append((vector(point) * TILE_SIZE + vector(32, 32) - self.offset))

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset  # Apply camera offset
            self.display_surface.blit(sprite.image, offset_pos)

        if len(points) > 1:
            print(f"Points: {points}")
            pygame.draw.lines(self.display_surface, (124, 252, 0), False, points, 5)
