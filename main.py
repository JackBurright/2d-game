# import asyncio
# import pygame
# from player import Player
# from enemy import Enemy
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_SCALE, HUMAN_SCALE, ZOMBIE_IMG, SOLDIER_IMG
# import time

# # pygame setup
# async def main():
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     clock = pygame.time.Clock()
#     running = True
#     dt = 0
#     game_score = 0
#     font = pygame.font.Font(None, 36)

#     # Sprite groups
#     projectiles = pygame.sprite.Group()
#     good_guys = pygame.sprite.Group()
#     enemies = pygame.sprite.Group()
#     player = Player(pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), img_path=SOLDIER_IMG, scale_factor= HUMAN_SCALE, projectile_group=projectiles)
#     good_guys.add(player)

#     enemy = Enemy(img_path=ZOMBIE_IMG, scale_factor=ZOMBIE_SCALE, good_guy=player)
#     enemies.add(enemy)
#     round = 1
    
#     while running:
#         # poll for events
#         # pygame.QUIT event means the user clicked X to close your window
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Game is over
#         if len(good_guys) == 0:
#             game_over_font = pygame.font.Font(None, 100)
#             game_over = game_over_font.render(f"You lost: {game_score}", True, "WHITE")
#             screen.blit(game_over, (SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-100))
#             pygame.display.flip()
#             await asyncio.sleep(3)
#             running = False

#         # Spawns next wave of zombies
#         if len(enemies) == 0:
#             round += 1
#             for _ in range(round):
#                 enemies.add(Enemy(img_path=ZOMBIE_IMG, scale_factor=ZOMBIE_SCALE, good_guy=player))

#         collisions = pygame.sprite.groupcollide(projectiles, enemies, True, True)
#         pygame.sprite.groupcollide(enemies, good_guys, False, True)
#         game_score += len(collisions)

#         # fill the screen with a color to wipe away anything from last frame
#         screen.fill("purple")

#         # Updates sprites
#         good_guys.update(dt)
#         enemies.update(dt, player)
#         projectiles.update(dt)

#         # Draws sprites
#         good_guys.draw(screen)
#         projectiles.draw(screen)
#         enemies.draw(screen)

#         # Write score
#         score_text = font.render(f"Score: {game_score}", True, "WHITE")
#         screen.blit(score_text, (10, 10))

#         # flip() the display to put your work on screen
#         pygame.display.flip()

#         # limits FPS to 60
#         # dt is delta time in seconds since last frame, used for framerate-independent physics.
#         dt = clock.tick(60) / 1000
#         await asyncio.sleep(0)

#     pygame.quit()

# asyncio.run(main())


import asyncio
import pygame
from player import Player
from enemy import Enemy
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_SCALE, HUMAN_SCALE, ZOMBIE_IMG, SOLDIER_IMG
import time

# Define game states
START, PLAYING, GAME_OVER = "START", "PLAYING", "GAME_OVER"

def reset_game():
    # Initialize game variables
    projectiles = pygame.sprite.Group()
    good_guys = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player(pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), img_path=SOLDIER_IMG, scale_factor=HUMAN_SCALE, projectile_group=projectiles)
    good_guys.add(player)
    for _ in range(1):  # Initial enemy
        enemy = Enemy(img_path=ZOMBIE_IMG, scale_factor=ZOMBIE_SCALE, good_guy=player)
        enemies.add(enemy)
    return projectiles, good_guys, enemies, player

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    game_state = START

    # Game variables
    game_score = 0
    round = 1
    dt = 0

    # Initialize game
    projectiles, good_guys, enemies, player = reset_game()

    while True:
        
        for event in pygame.event.get():
            # print(game_state, len(enemies),len(good_guys))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and game_state in {START, GAME_OVER}:
                # print(event.type)
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                    game_score = 0
                    round = 1
                    projectiles, good_guys, enemies, player = reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

        if game_state == START:
            screen.fill("black")
            start_text = font.render("Press space to start", True, "WHITE")
            screen.blit(start_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2))
            pygame.display.flip()
            await asyncio.sleep(0)
            continue

        if game_state == PLAYING:
            # Game is over
            if len(good_guys) == 0:
                game_state = GAME_OVER
                continue

            # Spawns next wave of zombies
            if len(enemies) == 0:
                round += 1
                for _ in range(round):
                    enemies.add(Enemy(img_path=ZOMBIE_IMG, scale_factor=ZOMBIE_SCALE, good_guy=player))

            collisions = pygame.sprite.groupcollide(projectiles, enemies, True, True)
            pygame.sprite.groupcollide(enemies, good_guys, False, True)
            game_score += len(collisions)

            # Fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            # Updates sprites
            good_guys.update(dt)
            enemies.update(dt, player)
            projectiles.update(dt)

            # Draws sprites
            good_guys.draw(screen)
            projectiles.draw(screen)
            enemies.draw(screen)

            # Write score
            score_text = font.render(f"Score: {game_score}", True, "WHITE")
            screen.blit(score_text, (10, 10))

            # Flip the display to put your work on screen
            pygame.display.flip()

            # Limits FPS to 60
            dt = clock.tick(60) / 1000
            await asyncio.sleep(0)

        elif game_state == GAME_OVER:
            screen.fill("black")
            game_over_font = pygame.font.Font(None, 100)
            game_over_text = game_over_font.render(f"You lost: {game_score}", True, "WHITE")
            restart_text = font.render("Press space to restart", True, "WHITE")
            quit_text = font.render("Press q to quit", True, "WHITE")
            screen.blit(game_over_text, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 100))
            screen.blit(restart_text, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 ))
            screen.blit(quit_text, (SCREEN_WIDTH / 2 - 110, SCREEN_HEIGHT / 2 + 50))
            pygame.display.flip()
            await asyncio.sleep(0)

asyncio.run(main())
