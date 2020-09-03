import random
import pygame
import time
import sys

pygame.init()

# CONSTANTS
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

display_width = 800
display_height = 600
baddie_width = 183

gameDisplay = pygame.display.set_mode((display_width, display_height))

gameDisplay.fill(RED)
pygame.display.set_caption('My Game')

clock = pygame.time.Clock()
image = pygame.image.load('/Users/eamonmckelvey/Desktop/ray-lewis-injury-ravens-10-15-12-16_9.jpg')
print(image.get_rect().size)

cop_image = pygame.image.load('/Users/eamonmckelvey/Desktop/police.jpg')
print(cop_image.get_rect().size)
cop_image.convert()
rect = cop_image.get_rect()
rect.center = display_width // 2, display_height // 2

pause = False


def baddie(x, y):
    gameDisplay.blit(image, (x, y))


def cop(cop_startx, cop_starty):
    gameDisplay.blit(cop_image, (cop_startx, cop_starty))


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 45)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    # pygame.display.update()

    print("Start : %s" % time.ctime())
    time.sleep(5)

    print("End : %s" % time.ctime())


def collide():
    largeText = pygame.font.SysFont("freesansbold.ttf", 115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        button_action("Play Again", 150, 450, 100, 50, GREEN, BRIGHT_GREEN, game_loop)
        button_action("Quit", 550, 450, 100, 50, RED, BRIGHT_RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, BLACK)
    gameDisplay.blit(text, (0, 0))


def button_action(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def unpause():
    global pause
    pause = False


def paused():
    #pause = True

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)

        gameDisplay.fill(WHITE)
        largeText = pygame.font.SysFont("freesansbold.ttf", 50)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button_action("Continue", 150, 450, 100, 50, GREEN, BRIGHT_GREEN, unpause)
        button_action("Quit", 550, 450, 100, 50, RED, BRIGHT_RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def quit_game():
    quit()


def game_intro():
    intro = True

    while intro == True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurface, TextRect = text_objects("My racing game", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurface, TextRect)

        mouse = pygame.mouse.get_pos()

        button_action("GO!", 150, 450, 100, 50, GREEN, BRIGHT_GREEN, game_loop)
        button_action("Quit", 550, 450, 100, 50, RED, BRIGHT_RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():

    global pause
    x = (display_width * 0.45)
    y = (display_height * 0.80)

    baddie_move = 0

    cop_startx = random.randrange(0, display_width - 57)
    cop_starty = -600
    cop_speed = 20

    count = 1
    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    baddie_move = -30

                elif event.key == pygame.K_RIGHT:
                    baddie_move = 30

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    baddie_move = 0

                if event.key == pygame.K_p:
                    pause = True
                    paused()

        x += baddie_move

        gameDisplay.fill(WHITE)

        cop(cop_startx, cop_starty)
        cop_starty += cop_speed
        baddie(x, y)
        things_dodged(dodged)

        # gameDisplay.blit(cop, rect)
        # pygame.draw.rect(gameDisplay, RED, rect, 1)

        if x > display_width - baddie_width or x < 0:
            baddie_move = 0

        if cop_starty > display_height:
            cop_starty = 0 - 103
            cop_startx = random.randrange(0, display_width)
            dodged += 1
            cop_speed += 10

        if y < cop_starty + 103:
            print('y crossover')

            if ((x > cop_startx) and (x < (cop_startx + 60)) or ((x + baddie_width) > cop_startx) and (
                    (x + baddie_width) < cop_startx + 60)):
                print('x crossover')
                collide()

        pygame.display.update()
        clock.tick(30)


game_intro()
game_loop()
pygame.quit()
quit()
