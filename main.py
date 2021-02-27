import pygame
import sys
import os
pygame.font.init()
pygame.mixer.init()

# naming constants with uppercase
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))    # defining window size
pygame.display.set_caption("Star Wars!")    # defining frame title
FPS = 60    # defining FPS
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
# here we have just created two new events and the numbers we added just specify that they are two different events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# few colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Loading Assets
SPACESHIP_RED_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_RED_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACESHIP_YELLOW_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(
    SPACESHIP_YELLOW_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "bullet_hit.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "bullet_fire.mp3"))


# main function
def main():
    red = pygame.Rect(750, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []    # To restrict player from spamming bullets
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        # this will make sure that our game runs at 60 FPS
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Firing Bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height/2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # Health
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


# Drawing function
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))     # Background
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # in pygame co-ordinates(0,0) is on top-left corner and not middle
    WIN.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))    # to load any surface (image, text) we use 'blit'
    WIN.blit(SPACESHIP_RED, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Yellow UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Yellow LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT-SPACESHIP_WIDTH:  # Yellow DOWN
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < (WIDTH/2) - (SPACESHIP_HEIGHT + 5):  # Yellow RIGHT
        yellow.x += VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Red UP
        red.y -= VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Red LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - SPACESHIP_WIDTH:  # Red DOWN
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Red RIGHT
        red.x += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)


if __name__ == "__main__":
    main()
