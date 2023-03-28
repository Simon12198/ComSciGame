import pygame, sys # import pygame and sys
from level_map import *


from pygame.locals import * # import pygame modules
clock = pygame.time.Clock() # set up the clock
pygame.init() # initiate pygame

pygame.display.set_caption('Better minecraft') # set the window name

WINDOW_SIZE = (SCREEN_WIDTH, screen_height) # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((rescaled_width, rescaled_height))

level = Level([], 'data/level', display)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                level.button_held()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                level.button_released()

    display.fill('red')  # fill the screen with black
    level.run()

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update() # update the screen
    clock.tick(60) # update the clock
