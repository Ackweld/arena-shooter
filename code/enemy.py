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
        self.direction = vector()
        self.speed = 300

        # Objects that the player should collide with
        self.collision_sprites = collision_sprites

        self.target = player.collision_rect
        self.path_find = path_find
        self.path = []

    def move(self, dt):
        self.collision_rect.x += self.direction.x * self.speed * dt
        # self.collison_check("horizontal")

        self.collision_rect.y += self.direction.y * self.speed * dt
        # self.collison_check("vertical")

    def face_direction(self):

        angle = self.direction.angle_to(vector(1, 0))

        rotated_image = pygame.transform.rotate(self.original_image, angle - 90)

        # Preserve the player's center position
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.collision_rect.center)

    # No need for collsision checking if enemy is path finding

    # def collison_check(self, axis):
    #     for sprite in self.collision_sprites:
    #         if sprite.rect.colliderect(self.collision_rect):
    #             if axis == "horizontal":
    #                 if (
    #                     self.collision_rect.left <= sprite.rect.right
    #                     and self.old_rect.left >= sprite.old_rect.right
    #                 ):
    #                     self.collision_rect.left = sprite.rect.right
    #                 if (
    #                     self.collision_rect.right >= sprite.rect.left
    #                     and self.old_rect.right <= sprite.old_rect.left
    #                 ):
    #                     self.collision_rect.right = sprite.rect.left
    #             else:  # vertical
    #                 if (
    #                     self.collision_rect.top <= sprite.rect.bottom
    #                     and self.old_rect.top >= sprite.old_rect.bottom
    #                 ):
    #                     self.collision_rect.top = sprite.rect.bottom
    #                 if (
    #                     self.collision_rect.bottom >= sprite.rect.top
    #                     and self.old_rect.bottom <= sprite.old_rect.top
    #                 ):
    #                     self.collision_rect.bottom = sprite.rect.top

    def follow_path(self):

        if self.path:
            # Convert path tile position to actual pixel position
            target_x = self.path[0][0] * TILE_SIZE + TILE_SIZE // 2
            target_y = self.path[0][1] * TILE_SIZE + TILE_SIZE // 2
            target_pos = vector(target_x, target_y)
            current_pos = vector(self.collision_rect.center)

            print(f"Target pos: {target_pos}")
            print(f"Current pos: {current_pos}")
            print(f"Distance: {target_pos.distance_to(current_pos)}")

            # If the enemy is close enough to the target, move to the next point
            if target_pos.distance_to(current_pos) < 5:
                self.path.pop(0)  # Remove the reached point
                if not self.path:
                    self.direction = vector(0, 0)  # Stop moving if no path left
                    return self.path
                
            # Calculate direction if path still exists
            direction_vector = target_pos - current_pos
            
            if direction_vector.length() > 0:  # Ensure it's not a zero vector
                self.direction = direction_vector.normalize()
            else:
                self.direction = vector(0, 0)  # Stop moving if there's no direction
                
    def get_path(self):
        return self.path

    def update(self, dt):
        if not self.path:
            self.path = self.path_find.a_star(
                (
                    round(self.collision_rect.x / TILE_SIZE),
                    round(self.collision_rect.y / TILE_SIZE),
                ),
                (round(self.target[0] / TILE_SIZE), round(self.target[1] / TILE_SIZE)),
            )
        self.follow_path()
        self.old_rect = self.collision_rect.copy()
        self.move(dt)
        self.face_direction()
