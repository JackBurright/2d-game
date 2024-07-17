import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT,MIN_SPAWN_DISTANCE
import random
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self, img_path, scale_factor,good_guy):
        super().__init__()
        self.original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * scale_factor),
             int(self.original_image.get_height() * scale_factor))
        )
        # pos = (int(SCREEN_WIDTH*random.random()), int(SCREEN_HEIGHT*random.random()))
        pos = self.spawn(good_guy)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.speed = 3

    #Makes sure enemys spawn enough distance away from player
    def spawn(self,good_guy):
        while True:
            loc = (int(SCREEN_WIDTH*random.random()), int(SCREEN_HEIGHT*random.random()))
            distance = math.sqrt((loc[0] - good_guy.rect.centerx)**2 + 
                              (loc[1] - good_guy.rect.centery)**2)
        
            if distance >= MIN_SPAWN_DISTANCE:
                return loc

    def update(self, dt,target):
        self.movement(dt,target)
    
    
    def movement(self,dt,target):
        direction_x = target.rect.centerx - self.rect.centerx
        direction_y = target.rect.centery - self.rect.centery

        # Calculate the distance to the target
        distance = math.sqrt(direction_x**2 + direction_y**2)

        # Normalize the direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Update position based on the direction and speed
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed
    
        