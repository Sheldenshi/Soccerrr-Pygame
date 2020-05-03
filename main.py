import pygame, sys, random

RED = (255, 0, 0)
GREEN = (102, 153, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (204, 204, 255)
PINK = (255, 153, 204)



pygame.init()
#mainClock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
pygame.display.set_caption("SOCCERRR")
kicker = pygame.transform.scale(pygame.image.load("kicker.png"), (50, 50))
kicker_rect = kicker.get_rect()
soccerball = pygame.transform.scale(pygame.image.load("soccerr.png"), (30, 30))
ball_rect = soccerball.get_rect()
keeper = pygame.transform.scale(pygame.image.load("keeper.png"), (30, 57))
keeper_rect = keeper.get_rect()
wall_image = pygame.transform.scale(pygame.image.load("wall.png"), (30, 18))
heart = pygame.transform.scale(pygame.image.load("heart.png"), (15, 14))

background = pygame.image.load("background.png")
textcolor = BLACK
window_width = 476
window_height = 736
ball_x_vel = 8
ball_y_vel = 8
keeper_vel = 2
score = 0
lives = [pygame.Rect(395, 26, 15, 14), pygame.Rect(413, 26, 15, 14), pygame.Rect(431, 26, 15, 14)]
level = 1
wall_max = 3
wall_min = 1
wall_vel_min = 0
wall_vel_max = 5
wall_spots = [136, 256, 376, 496, 616]
top_socre = 0
walls = []

window = pygame.display.set_mode((window_width, window_height))

def terminate():
    pygame.quit()
    sys.exit()

def wait_for_player_to_presskey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    return
def hit_check(ball_rect, keeper_rect, walls):
    for wall in walls:
        if ball_rect.colliderect(wall['rect']):
            return True
    if ball_rect.colliderect(keeper_rect):
        return True
    else:
        return False

def draw_text(text, font, surface, x, y):
    textobj= font.render(text, 1, textcolor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

""" adding people into walls """
def making_walls(walls):
    def wall_for_a_row(y, wall_vel):
        number_of_people = random.randint(wall_min, wall_max)
        x_starting = random.randint(0, window_width - 30 * number_of_people)
        while number_of_people > 0:
            newwall = {'rect':pygame.Rect(x_starting, y, 30, 18),
                        'speed': wall_vel,
                      }
            walls.append(newwall)
            number_of_people -= 1
            x_starting += 30
    for y in wall_spots:
        wall_for_a_row(y, random.randint(wall_vel_min, wall_vel_max))






#show the start screen
window.fill(GREEN)
draw_text('SOCCERRR', (pygame.font.SysFont(None, 48)), window, (window_width / 3)- 35, (window_height / 3))
window.blit(soccerball, (window_width - 155, (window_height / 3)))
draw_text('Press a key to start', (pygame.font.SysFont(None, 24)), window, (window_width / 3), window_height - 100)
pygame.display.update()
wait_for_player_to_presskey()

while True:
    pygame.time.delay(100)
    ball_rect.center = (window_width / 2, window_height - 50)
    kicker_rect.center = (window_width / 2, window_height - 20)
    keeper_rect.center = (window_width / 2, window_height - 705)
    move_left = move_right = shoot = False
    walls.clear()
    making_walls(walls)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            """ moving the ball """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_right = False
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_left = False
                    move_right = True
                if event.key == pygame.K_SPACE:
                    shoot = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
        """ checking if the ball had hit anything"""
        if hit_check(ball_rect, keeper_rect, walls) or (ball_rect.top < 5 and (ball_rect.left <= 140 or ball_rect.right >= 337)):
            lives.pop()
            run = False
        """ creating walls"""

        if ball_rect.top > 0 and not hit_check(ball_rect, keeper_rect, walls):
            if ball_rect.top > 50:
                if move_left and ball_rect.left > 0:
                    ball_rect.move_ip(-1 * ball_x_vel, 0)
                if move_right and ball_rect.right < window_width:
                    ball_rect.move_ip(ball_x_vel, 0)
            """ moving the kicker """
            if not shoot:
                if move_left and kicker_rect.left > 0:
                    kicker_rect.move_ip(-1 * ball_x_vel, 0)
                if move_right and kicker_rect.right < window_width:
                    kicker_rect.move_ip(ball_x_vel, 0)
            if shoot:
                ball_rect.move_ip(0, -1 * ball_y_vel)
            """ moving the keeper """
            if keeper_rect.right > 333:
                keeper_vel *= -1
            if keeper_rect.left < 143:
                keeper_vel *= -1
            keeper_rect.move_ip(keeper_vel, 0)
            """ move walls """
            for wall in walls:
                if wall['rect'].right > 476:
                    wall['speed'] = wall['speed'] * -1
                if wall['rect'].left < 0:
                    wall['speed'] = wall['speed'] * -1
                wall['rect'].move_ip(wall['speed'], 0)


        if ball_rect.top < 5 and ball_rect.left > 125 and ball_rect.right < 350:
            score += 1
            if score > top_socre:
                top_socre = score
            run = False

        window.blit(background,(0, 0))
        draw_text('Score: %s' %(score), (pygame.font.SysFont(None, 24)), window, 10, 6)
        draw_text('Top Score: %s' %(top_socre), (pygame.font.SysFont(None, 24)), window, 10, 25)
        draw_text('Lives:', (pygame.font.SysFont(None, 24)), window, 345, 25)
        draw_text('Level: %s' %(level), (pygame.font.SysFont(None, 24)), window, 345, 6)
        for live in lives:
            window.blit(heart, live)
        for wall in walls:
            window.blit(wall_image, wall['rect'])
        window.blit(keeper, keeper_rect)
        window.blit(kicker,kicker_rect)
        window.blit(soccerball, ball_rect)

        pygame.display.update()

    if not lives:
        draw_text('GAME OVER', (pygame.font.SysFont(None, 48)), window, (window_width / 3)- 25, (window_height / 3) + 65)
        draw_text('Press a key to start', (pygame.font.SysFont(None, 24)), window, (window_width / 3), window_height - 160)
        pygame.display.update()
        ball_x_vel = 8
        ball_y_vel = 8
        keeper_vel = 2
        score = 0
        lives = [pygame.Rect(395, 26, 15, 14), pygame.Rect(413, 26, 15, 14), pygame.Rect(431, 26, 15, 14)]
        level = 1
        wall_max = 6
        wall_min = 1
        wall_vel_min = 0
        wall_vel_max = 5
        wait_for_player_to_presskey()

    if score > 0:
        level = 2
        ball_x_vel = 9
        ball_y_vel = 9
        keeper_vel = 3
        wall_max = 5
        wall_min = 2
        wall_vel_min = 1
        wall_vel_max = 5
    if score > 1:
        level = 3
        ball_x_vel = 10
        ball_y_vel = 10
        keeper_vel = 3
        wall_max = 6
        wall_min = 3
        wall_vel_min = 1
        wall_vel_max = 6
    if score > 2:
        level = 4
        ball_x_vel = 10
        ball_y_vel = 11
        keeper_vel = 4
        wall_max = 7
        wall_min = 3
        wall_vel_min = 3
        wall_vel_max = 7
    if score > 3:
        levle = 5
        ball_x_vel = 12
        ball_y_vel = 14
        keeper_vel = 6
        wall_max = 8
        wall_min = 4
        wall_vel_min = 5
        wall_vel_max = 8
    if score > 6:
        level = 6
        ball_x_vel = 14
        ball_y_vel = 16
        keeper_vel = 8
        wall_max = 9
        wall_min = 5
        wall_vel_min = 6
        wall_vel_max = 10
    if score > 8:
        level = 7
        ball_x_vel = 16
        ball_y_vel = 18
        keeper_vel = 10
        wall_max = 10
        wall_min = 6
        wall_vel_min = 7
        wall_vel_max = 11




pygame.quit()
