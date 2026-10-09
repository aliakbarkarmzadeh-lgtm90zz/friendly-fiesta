import pygame
import random

pygame.init()

# تمام صفحه
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = screen.get_size()
clock = pygame.time.Clock()

# بازیکن
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 220, 50, 50)

# دشمن
enemy = pygame.Rect(
    random.randint(30, WIDTH - 80),
    80,
    50,
    50
)

bullets = []
score = 0

game_started = False
game_over = False
running = True

# دکمه شروع
start_button = pygame.Rect(
    WIDTH // 2 - 150,
    HEIGHT // 2 - 40,
    300,
    80
)

# دکمه‌های پایین
button_y = HEIGHT - 130

left_button = pygame.Rect(20, button_y, 150, 100)
right_button = pygame.Rect(190, button_y, 150, 100)
shoot_button = pygame.Rect(WIDTH - 170, button_y, 150, 100)

font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 80)

while running:

    shoot = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if not game_started:

                if start_button.collidepoint(x, y):
                    game_started = True

            elif not game_over:

                if left_button.collidepoint(x, y):
                    player.x -= 50

                elif right_button.collidepoint(x, y):
                    player.x += 50

                elif shoot_button.collidepoint(x, y):
                    shoot = True

    if game_started and not game_over:

        # محدود کردن بازیکن
        if player.left < 0:
            player.left = 0

        if player.right > WIDTH:
            player.right = WIDTH

        # شلیک
        if shoot:
            bullets.append(
                pygame.Rect(
                    player.centerx - 6,
                    player.top - 25,
                    12,
                    25
                )
            )

        # حرکت دشمن
        enemy.y += 5

        if enemy.top > HEIGHT:
            enemy.x = random.randint(30, WIDTH - 80)
            enemy.y = 80

        # گلوله‌ها
        for bullet in bullets[:]:

            bullet.y -= 12

            if bullet.bottom < 0:
                bullets.remove(bullet)

            elif bullet.colliderect(enemy):

                bullets.remove(bullet)

                score += 1

                enemy.x = random.randint(30, WIDTH - 80)
                enemy.y = 80

        # برخورد
        if player.colliderect(enemy):
            game_over = True

    # پس‌زمینه
    screen.fill((8, 12, 25))

    # ستاره‌ها
    for i in range(60):
        x = (i * 97) % WIDTH
        y = (i * 53) % HEIGHT
        pygame.draw.circle(screen, (120, 140, 180), (x, y), 2)

    # صفحه شروع
    if not game_started:

        title = big_font.render(
            "MINI BATTLE",
            True,
            (0, 180, 255)
        )

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150)
        )

        pygame.draw.rect(
            screen,
            (0, 140, 255),
            start_button,
            border_radius=15
        )

        start_text = font.render(
            "START GAME",
            True,
            (255, 255, 255)
        )

        screen.blit(
            start_text,
            (
                WIDTH // 2 - start_text.get_width() // 2,
                HEIGHT // 2 - 15
            )
        )

    else:

        # بازیکن
        pygame.draw.rect(
            screen,
            (0, 150, 255),
            player,
            border_radius=10
        )

        # هسته بازیکن
        pygame.draw.circle(
            screen,
            (100, 220, 255),
            player.center,
            12
        )

        # دشمن
        pygame.draw.rect(
            screen,
            (255, 50, 50),
            enemy,
            border_radius=10
        )

        # هسته دشمن
        pygame.draw.circle(
            screen,
            (255, 180, 0),
            enemy.center,
            12
        )

        # گلوله‌ها
        for bullet in bullets:

            pygame.draw.rect(
                screen,
                (255, 220, 0),
                bullet,
                border_radius=5
            )

        # دکمه چپ
        pygame.draw.rect(
            screen,
            (50, 60, 80),
            left_button,
            border_radius=15
        )

        # دکمه راست
        pygame.draw.rect(
            screen,
            (50, 60, 80),
            right_button,
            border_radius=15
        )

        # دکمه شلیک
        pygame.draw.rect(
            screen,
            (180, 40, 40),
            shoot_button,
            border_radius=15
        )

        screen.blit(
            font.render("LEFT", True, (255,255,255)),
            (left_button.centerx - 35, left_button.centery - 20)
        )

        screen.blit(
            font.render("RIGHT", True, (255,255,255)),
            (right_button.centerx - 45, right_button.centery - 20)
        )

        screen.blit(
            font.render("FIRE", True, (255,255,255)),
            (shoot_button.centerx - 30, shoot_button.centery - 20)
        )

        # امتیاز
        score_text = font.render(
            "SCORE: " + str(score),
            True,
            (255, 255, 255)
        )

        screen.blit(score_text, (25, 25))

        # Game Over
        if game_over:

            text = big_font.render(
                "GAME OVER",
                True,
                (255, 70, 70)
            )

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - 50
                )
            )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
