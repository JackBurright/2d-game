import pygame
from projectile import Projectile
from config import SCREEN_HEIGHT, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, scale_factor,projectile_group):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * scale_factor),
             int(self.original_image.get_height() * scale_factor))
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.pos = pygame.Vector2(pos)
        self.speed = 300
        self.projectile_group = projectile_group
        self.time_since_last_shot = 0
        self.shot_cooldown = 0.5

    def update(self, dt):
        self.movement(dt)
        self.shoot_projectile(dt)

    def movement(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt
        self.rect.center = self.pos

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            print("player died")
            self.kill()

    def shoot_projectile(self,dt):
        self.time_since_last_shot += dt
        keys = pygame.key.get_pressed()
        if self.time_since_last_shot > self.shot_cooldown:
            if keys[pygame.K_UP]:
                self.projectile_group.add(Projectile(self.pos.x, self.pos.y,0))
                self.time_since_last_shot =0
            elif keys[pygame.K_LEFT]:
                self.projectile_group.add(Projectile(self.pos.x, self.pos.y,1))
                self.time_since_last_shot = 0
            elif keys[pygame.K_DOWN]:
                self.projectile_group.add(Projectile(self.pos.x, self.pos.y,2))
                self.time_since_last_shot = 0
            elif keys[pygame.K_RIGHT]:
                self.projectile_group.add(Projectile(self.pos.x, self.pos.y,3))
                self.time_since_last_shot = 0
