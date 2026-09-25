import asyncio
import pygame
from constants import PLAYER_LIVES, SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

CONTROLS_HINT = "W/A/S/D or arrow keys to move  ·  Space to shoot"


def draw_text(screen, font, text, color="white", **position) -> None:
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(**position))


# async so pygbag can run the game in a browser: the loop yields once per frame
# with `await asyncio.sleep(0)`. It runs the same way on desktop.
async def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    hud_font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 96)
    dt = 0.0

    # create all groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # set all containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    def new_game() -> Player:
        for group in (updatable, drawable, asteroids, shots):
            group.empty()
        AsteroidField()
        return Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    player = new_game()
    score = 0
    lives = PLAYER_LIVES
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (
                game_over
                and event.type == pygame.KEYDOWN
                and event.key in (pygame.K_r, pygame.K_RETURN)
            ):
                player = new_game()
                score = 0
                lives = PLAYER_LIVES
                game_over = False

        updatable.update(dt)

        # Remove anything that has drifted off-screen so the groups don't grow forever
        for sprite in (*asteroids, *shots):
            if sprite.is_offscreen():
                sprite.kill()

        if not game_over and not player.is_invulnerable():
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    lives -= 1
                    if lives == 0:
                        player.kill()
                        game_over = True
                    else:
                        player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    break

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    score += asteroid.points()
                    asteroid.split()
                    shot.kill()
                    # One shot per asteroid, so it can't split twice in one frame
                    break

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        draw_text(screen, hud_font, f"Score: {score}", topleft=(20, 20))
        draw_text(screen, hud_font, f"Lives: {lives}", topright=(SCREEN_WIDTH - 20, 20))
        draw_text(screen, hud_font, CONTROLS_HINT, color="gray50", midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 16))

        if game_over:
            center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            draw_text(screen, title_font, "GAME OVER", center=(center_x, center_y - 60))
            draw_text(screen, hud_font, f"Final score: {score}", center=(center_x, center_y + 10))
            draw_text(screen, hud_font, "Press R or Enter to play again", center=(center_x, center_y + 50))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
