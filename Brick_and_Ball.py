import pygame

pygame.init()
clock = pygame.time.Clock()
screen_width = 500
screen_height = 560
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("Background.png")
game_over_image = pygame.image.load("Game Over.png")
ball_image = pygame.image.load("Ball.png")
icon = pygame.image.load("Logo.png")

pygame.mixer.music.load("Game Music.wav")
pygame.mixer.music.play(-1)
pygame.display.set_caption("Brick and Ball")
pygame.display.set_icon(icon)

font_score_play = pygame.font.SysFont("Bell MT", 35)
font_score_over = pygame.font.SysFont("Arial Rounded MT Bold", 70)
font_title = pygame.font.SysFont("Times New Roman", 60)
font_credit = pygame.font.SysFont("Times New Roman", 35)
font_button = pygame.font.SysFont("Comic Sans MS", 50)

def update_bricks():
    global bricks, brick_width, brick_height
    bricks = []
    brick_width = 45
    brick_height = 10
    for i in range(6):
        for j in range(12):
            bricks.append([27 + i * 80, 15 + j * 20])

def update_ball():
    global ball_x, ball_y, ball_speed, ball_x_speed, ball_y_speed
    ball_x = 240
    ball_y = 485
    ball_speed = 1
    ball_x_speed = ball_speed
    ball_y_speed = -ball_speed

def update_base():
    global base_width, base_height, base_x, base_y, base_speed
    base_width = 80
    base_height = 10
    base_x = 210
    base_y = 505
    base_speed = 0

def start_game():
    global score_value
    score_value = 0
    update_bricks()
    update_ball()
    update_base()

white = (255, 255, 255)
blue = (135, 206, 235)
violet = (148, 0, 211)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

running = True
state = ""

while running:

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if state == "":
                if 200 < mouse[0] < 290 and 455 < mouse[1] < 510:
                    state = "play"
                    start_game()

            elif state == "over":

                if 180 < mouse[0] < 285 and 465 < mouse[1] < 515:
                    running = False
                    
                elif 150 < mouse[0] < 330 and 365 < mouse[1] < 410:
                    state = "play"
                    start_game()

        elif event.type == pygame.KEYDOWN:

            if state == "play":

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    base_speed = -1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    base_speed = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                base_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                base_speed = 0

    if state == "play":
        
        screen.fill(white)
        screen.blit(background_image, (10, 0))
        ball_rect = ball_image.get_rect(topleft = (ball_x, ball_y))

        for i in bricks:
            brick_rect = pygame.Rect(i[0], i[1], brick_width, brick_height)
            pygame.draw.rect(screen, blue, brick_rect)

            if brick_rect.colliderect(ball_rect):
                pygame.mixer.Sound("Brick Break.wav").play()
                bricks.remove(i)
                score_value += 1

                if abs(brick_rect.top - ball_rect.bottom) < 10:
                    ball_y_speed *= -1
                if abs(brick_rect.bottom - ball_rect.top) < 10:
                    ball_y_speed *= -1
                if abs(brick_rect.left - ball_rect.right) < 10:
                    ball_x_speed *= -1
                if abs(brick_rect.right - ball_rect.left) < 10:
                    ball_x_speed *= -1
            
        screen.blit(ball_image, (ball_x, ball_y))
        base_rect = pygame.Rect(base_x, base_y, base_width, base_height)
        pygame.draw.rect(screen, green, base_rect)

        base_x += base_speed
        if base_x < 15:
            base_x = 15
        elif base_x > 405:
            base_x = 405

        ball_x += ball_x_speed
        ball_y += ball_y_speed
        
        if ball_y <= 0:
            ball_y_speed *= -1
        if ball_x <= 10 or ball_x >= 470:
            ball_x_speed *= -1

        if ball_rect.colliderect(base_rect) and ball_y_speed > 0:
            pygame.mixer.Sound("Ball Deflection.wav").play()
            ball_y_speed *= -1
            
        if ball_y >= 510:
            pygame.mixer.Sound("Game Over.wav").play()
            state = "over"
        if len(bricks) == 0:
            pygame.mixer.Sound("Winner.wav").play()
            state = "over"

        score = font_score_play.render("Score : " + str(score_value), True, black)
        screen.blit(score, (200, 530))
    
    elif state == "":

        game_title = font_title.render("Brick  and  Ball", True, blue)
        name = font_credit.render("Made By : Sunny Kumar", True, yellow)
        branch = font_credit.render("BE  CSE", True, yellow)
        year = font_credit.render("2021 - 2025", True, yellow)

        if 200 < mouse[0] < 290 and 455 < mouse[1] < 510:
            play = font_button.render("Play", True, green)
        else:
            play = font_button.render("Play", True, white)

        screen.blit(game_title, (55, 50))
        screen.blit(name, (60, 220))
        screen.blit(branch, (220, 270))
        screen.blit(year, (220, 320))
        screen.blit(play, (200, 445))

    elif state == "over":

        if 150 < mouse[0] < 330 and 365 < mouse[1] < 410:
            restart = font_button.render("Restart", True, green)
        else:
            restart = font_button.render("Restart", True, violet)

        if 180 < mouse[0] < 285 and 465 < mouse[1] < 515:
            quit = font_button.render("Quit", True, green)
        else:
            quit = font_button.render("Quit", True, violet)
        
        score = font_score_over.render("Score : " + str(score_value), True, black)
        screen.blit(game_over_image, (0, 0))
        screen.blit(score, (140, 250))
        screen.blit(restart, (150, 350))
        screen.blit(quit, (180, 450))

    clock.tick(240)
    pygame.display.update()