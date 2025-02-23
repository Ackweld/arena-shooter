from settings import *
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # Load original image
        self.original_image = pygame.image.load(
            join("..", "graphics", "player", "player.png")
        ).convert_alpha()

        self.image = self.original_image.copy()

        # Collision rectangle (does NOT rotate)
        self.collision_rect = self.image.get_rect(center=pos)
        # Used to check from which direction the player came from before collision
        self.old_rect = self.collision_rect.copy()

        # The actual sprite rect (for rendering)
        self.rect = self.collision_rect.copy()

        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Movement
        self.direction = vector()
        self.speed = 400

        # Objects that the player should collide with
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_w]:
            input_vector.y -= 1
        if keys[pygame.K_s]:
            input_vector.y += 1
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self, dt):
        self.collision_rect.x += self.direction.x * self.speed * dt
        self.collison("horizontal")

        self.collision_rect.y += self.direction.y * self.speed * dt
        self.collison("vertical")

    def face_mouse_cursor(self):

        mouse_pos = vector(pygame.mouse.get_pos())
        screen_center = vector(self.half_w, self.half_h)

        # Calculate direction from screen center to mouse
        direction = mouse_pos - screen_center

        # Calculate the angle relative to the rightward direction
        angle = direction.angle_to(vector(1, 0))

        # Rotate the image while keeping the collision rect unchanged
        rotated_image = pygame.transform.rotate(self.original_image, angle - 90)

        # Preserve the player's center position
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.collision_rect.center)

    def collison(self, axis):
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

    def update(self, dt):
        self.old_rect = self.collision_rect.copy()
        self.input()
        self.move(dt)
        self.face_mouse_cursor()
