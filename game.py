# Example file showing a circle moving on screen
import pygame
from player import Player
from enemy import Enemy
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_SCALE, HUMAN_SCALE, ZOMBIE_IMG,SOLDIER_IMG
import time
# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
game_score = 0
font = pygame.font.Font(None, 36)

#Sprite groups
projectiles = pygame.sprite.Group()
good_guys = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2),img_path=SOLDIER_IMG, scale_factor= HUMAN_SCALE,projectile_group=projectiles)
good_guys.add(player)

enemy = Enemy(img_path=ZOMBIE_IMG,scale_factor=ZOMBIE_SCALE, good_guy=player)

enemies.add(enemy)
round = 1
while running:
    
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Game is over
    if len(good_guys) == 0:
        game_over_font = pygame.font.Font(None, 100)
        game_over = game_over_font.render(f"You lost: {game_score}", True, "WHITE")
        screen.blit(game_over, (SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-100))
        pygame.display.flip()
        time.sleep(3)
        running = False


    #Spawns next wave of zombies
    if len(enemies) == 0:
        round += 1
        for _ in range(round):
            enemies.add(Enemy(img_path=ZOMBIE_IMG,scale_factor=ZOMBIE_SCALE, good_guy=player))

    collisions = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    pygame.sprite.groupcollide(enemies,good_guys,False,True)
    game_score += len(collisions)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #Updates sprites
    good_guys.update(dt)
    enemies.update(dt,player)
    projectiles.update(dt)

    #Draws sprites
    good_guys.draw(screen)
    projectiles.draw(screen)
    enemies.draw(screen)

    #Write score.
    score_text = font.render(f"Score: {game_score}", True, "WHITE")
    screen.blit(score_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()