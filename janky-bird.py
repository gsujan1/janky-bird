import pygame
import random
import time

pygame.init()

# screen dimensions
WIDTH = 550
HEIGHT = 800

# some basic colors for us to work with
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# sound load in
flap_wing = pygame.mixer.Sound('Butterfly-Wings.wav')
pygame.mixer.music.load('Neon-Runner_Looping.wav')

# game display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Janky Bird')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

# initializes our (in essence) fps counter
clock = pygame.time.Clock()

def add_bird(color, x_pos, y_pos, rad_size):
    pygame.draw.circle(screen, color, (x_pos, y_pos), rad_size)

def add_pipe(x_pos, y_pos, obsh, obsw, color):
    pygame.draw.rect(screen, color, [x_pos, y_pos, obsh, obsw])

def pipes_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Score: ' + str(count), True, WHITE)
    screen.blit(text, (0,0))

def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    textSurf, textRect = text_objects(text, largeText)
    textRect.center = ((WIDTH/2), (HEIGHT/2))
    screen.blit(textSurf, textRect)
    pygame.display.update()
    # restart game loop after 1.5 seconds
    time.sleep(1.5)
    game_loop()

def game_over():
    message_display('GAME OVER')

def game_loop():

    # pipes dodged counter
    dodged = 0

    # ground vars
    ground_x = 0
    ground_y = HEIGHT - 10
    ground_h = WIDTH
    ground_w = 10

    # bird vars
    x = 75
    y = 400
    size = 15

    # gravity for now
    y_change = 6

    # pipe vars
    pipe_x = 400
    pipe_y = random.randrange(HEIGHT * 0.22, HEIGHT)
    pipe_w = 75
    pipe_h = HEIGHT - pipe_y - 10
    pipe_speed = 5 # can slowly increase this, see line 125

    # pipe top pair
    pipe_yt = pipe_y - 150
    pipe_ht = 0 - pipe_yt

    # music
    pygame.mixer.music.play(-1)

    # EVENT HANDLER LOOP
    gameExit = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print('spacebar pressed')
                    pygame.key.set_repeat(200000, 2000000)
                    y_change = -8
                    # play Sound
                    pygame.mixer.Sound.play(flap_wing)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    y_change = 6

        # draws black background
        screen.fill(BLACK)
        # draws ground
        add_pipe(ground_x, ground_y, ground_h, ground_w, WHITE)
        # adds top and bottom pipes
        add_pipe(pipe_x, pipe_y, pipe_w, pipe_h, GREEN)
        add_pipe(pipe_x, pipe_yt, pipe_w, pipe_ht, GREEN)
        # adds our janky bird
        add_bird(YELLOW, x, y, size)
        pipes_dodged(dodged)


        # moves pipe pairs left and redraws them at
        # end of screen when pipe moves out of screen range
        pipe_x -= pipe_speed
        if pipe_x <= -50:
            pipe_x = WIDTH + 50
            pipe_y = random.randrange(HEIGHT * 0.22, HEIGHT)
            pipe_h = HEIGHT - pipe_y - 10 # 10 included for ground clearance
            pipe_yt = pipe_y - 150
            pipe_ht = 0 - pipe_yt
            # dodge counter
            dodged += 1
            # pipe speed increment
            # pipe_speed += 0.5

        # if bird hits ground or top of screen, game over
        y += y_change
        if y >= (HEIGHT - 10) or y <= 0:
            # stop music
            pygame.mixer.stop()
            game_over()

        # collision logic
        # maybe want to use COLLIDERECT method
        # only detects collision with center of bird
        if x >= pipe_x and x <= pipe_x + pipe_w:
            if y <= pipe_yt - 10 or y >= pipe_y:
                # stop music
                pygame.mixer.stop()
                game_over()

        pygame.display.update()

        clock.tick(60)

game_loop()
