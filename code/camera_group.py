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

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset  # Apply camera offset
            self.display_surface.blit(sprite.image, offset_pos)

        # Draw the enemy A* path. Used for debugging.
        enemy_path = enemy.get_path()
        # print(
        #     f"Enemy: {enemy.get_enemy_to_player_vector()[0]}, Player: {enemy.get_enemy_to_player_vector()[1]}"
        # )
        pygame.draw.line(
            self.display_surface,
            (255, 0, 0),
            vector(enemy.get_enemy_to_player_vector()["enemy"])
            + vector(TILE_SIZE / 2, TILE_SIZE / 2)
            - self.offset,
            vector(enemy.get_enemy_to_player_vector()["player"])
            + vector(TILE_SIZE / 2, TILE_SIZE / 2)
            - self.offset,
            5,
        )

        points = []
        for point in enemy_path:
            points.append((vector(point) * TILE_SIZE + vector(TILE_SIZE / 2, TILE_SIZE / 2) - self.offset))
        if len(points) > 1:
            pygame.draw.lines(self.display_surface, (124, 252, 0), False, points, 5)
