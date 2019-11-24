from pygame import *

DIM = (1280, 800)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

color = GREEN

screen = display.set_mode(DIM)
""" start point """
x = 0
y = 0
""" velocity of the ball """
vx = 2
vy = 3
""" acc. of the ball """
ax = .4
ay = 3

running = True

while running:

    for e in event.get():
        if e.type == QUIT:
            running = False
        #if e.type == MOUSEBUTTONDOWN:
            #color = RED

    screen.fill(WHITE)

    vx = int(vx + ax)
    vy = int(vy + ay)
    x = int(x + vx)
    y = int(y + vy)

    if y > 800:
        vy *= -1
    if x > 1280:
        vx *= -1

    draw.circle(screen, color, (x, y), 30)
    display.flip()

quit()
