from settings import *
from os.path import join
import heapq


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player, path_find):
        super().__init__(groups)

        self.original_image = pygame.image.load(
            join("..", "graphics", "enemy", "enemy.png")
        ).convert_alpha()

        self.image = self.original_image.copy()

        # Collision rectangle (does NOT rotate)
        self.collision_rect = self.image.get_frect(center=pos)
        # Used to check from which direction the player came from before collision
        self.old_rect = self.collision_rect.copy()

        # The actual sprite rect (for rendering)
        self.rect = self.collision_rect.copy()

        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # self.rect = self.image.get_rect(center=pos)
        # Movement
        self.direction = vector(1, 0)
        self.speed = 400

        # Objects that the player should collide with
        self.collision_sprites = collision_sprites

        self.target = player.collision_rect
        self.path_find = path_find
        self.path = []

    def move(self, dt):
        self.collision_rect.x += self.direction.x * self.speed * dt
        self.collison_check("horizontal")

        self.collision_rect.y += self.direction.y * self.speed * dt
        self.collison_check("vertical")

    def face_direction(self):

        angle = self.direction.angle_to(vector(1, 0))

        rotated_image = pygame.transform.rotate(self.original_image, angle - 90)

        # Preserve the player's center position
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.collision_rect.center)

    def collison_check(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.collision_rect):
                if axis == "horizontal":
                    if (
                        self.collision_rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.collision_rect.left = sprite.rect.right
                    if (
                        self.collision_rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.collision_rect.right = sprite.rect.left
                else:  # vertical
                    if (
                        self.collision_rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.collision_rect.top = sprite.rect.bottom
                    if (
                        self.collision_rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.collision_rect.bottom = sprite.rect.top

    def follow_path(self):
        return self.path

    def update(self, dt):
        print(f"TARGET: {self.target.centerx, self.target.centery}")
        # self.path = self.path_find.a_star(vector(self.collision_rect.x, self.collision_rect.y), vector(9, 1))
        # print(f"X: {self.collision_rect.centerx}, Y: {self.collision_rect.centery}")
        self.path = self.path_find.a_star(
            vector(
                self.collision_rect.centerx // TILE_SIZE,
                self.collision_rect.centery // TILE_SIZE,
            ),
            vector(self.target[0] // TILE_SIZE, self.target[1] // TILE_SIZE),
        )
        self.old_rect = self.collision_rect.copy()
        self.move(dt)
        self.face_direction()
