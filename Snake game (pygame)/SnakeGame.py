import pygame
import random
import os

pygame.mixer.init()

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load("welcomebg.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

goimg = pygame.image.load("go.jpg")
goimg = pygame.transform.scale(goimg, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snakes by Gizmo")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 229))
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Welcome to Snakes by Gizmo", black, screen_width/4.8, screen_height/5.3)
        text_screen("Press Space to play", red, screen_width / 3.5, screen_height /1.2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('East of Tunesia - Kevin MacLeod.mp3')
                    # pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 10
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)
    score = 0
    init_velocity = 5
    fps = 60

    # if not os.path.exists("highscore.txt"):
    #     with open("highscore.txt", "w") as f:
    #         f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(goimg, (0, 0))
            text_screen("Game over!! Press enter to continue.", red, screen_width/8, screen_height/2.3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(0, screen_width)
                food_y = random.randint(0, screen_height)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  High Score: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
                pygame.mixer.music.load('Beep Short .mp3')
                pygame.mixer.music.play()

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Big Explosion Cut Off.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('Big Explosion Cut Off.mp3')
                pygame.mixer.music.play()

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
