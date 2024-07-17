import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PROJECTILE_SCALE, PROJECTILE_IMG

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.original_image = pygame.image.load(PROJECTILE_IMG).convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * PROJECTILE_SCALE),
             int(self.original_image.get_height() * PROJECTILE_SCALE))
        )
        # self.image.fill("black")
        self.rect = self.image.get_rect(center=(x, y))
        self.bullet_direction = direction
        if self.bullet_direction == 1:
            self.image = pygame.transform.rotate(self.image,90)
        elif self.bullet_direction == 2:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.bullet_direction == 3:
            self.image = pygame.transform.rotate(self.image, 270)

    def update(self,dt):
        # Move projectile 
        if self.bullet_direction == 0:
            self.rect.y -= 8
        elif self.bullet_direction == 1:
            self.rect.x -= 8
        elif self.bullet_direction == 2:
            self.rect.y += 8
        elif self.bullet_direction == 3:
            self.rect.x += 8
        
        # Remove projectile when it goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()