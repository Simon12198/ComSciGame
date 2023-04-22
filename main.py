import pygame, sys  # import pygame and sys
from level_map import *
import button
from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame
clock = pygame.time.Clock()  # set up the clock
pygame.display.set_caption('Fatal Echo')  # set the window name

WINDOW_SIZE = (SCREEN_WIDTH, screen_height)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen

display = pygame.Surface((rescaled_width, rescaled_height))
# define colours
TEXT_COL = (255, 255, 255)
BGCOLOUR = (0, 128, 255)
MENUCOLOUR = (76, 0, 153)

# load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

# create button instances
#to remember order of function:
#(self, x, y, image, scale)
resume_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 1/4, resume_img, 1.2)
options_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 2/4, options_img, 1.2)
quit_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 3/4, quit_img, 1.2)
video_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 1/4 - 100, video_img, 1.2)
audio_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 2/4 - 100, audio_img, 1.2)
keys_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 3/4 - 100, keys_img, 1.2)
back_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 7/8 - 50, back_img, 1.2)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def screen_text(text, fontsize, color, x, y):
    font = pygame.font.SysFont("arial", fontsize)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
menu_mode = "main"
clicked = False

level = Level([], 'data/level', display)

RUNNING, PAUSE, STARTSCREEN, ENDSCREEN = 0, 1, 2, 3
state = STARTSCREEN
while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                level.button_held()
            if e.key == K_ESCAPE:
                state = PAUSE
            if e.type == KEYUP:
                if e.key == K_SPACE:
                    level.button_released()
            if state == STARTSCREEN:
                if pygame.key.get_pressed():
                    state = RUNNING
        if e.type == pygame.MOUSEBUTTONUP:
            clicked = False

    else:
        if state == RUNNING:
            display.fill('red')
            level.run()
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()  # update the screen
        elif state == PAUSE:
            screen.fill(MENUCOLOUR)
            if menu_mode == "main":
                # draw pause screen buttons
                if resume_button.draw(screen) and clicked == False:
                    state = RUNNING
                    clicked = True
                if options_button.draw(screen) and clicked == False:
                    menu_mode = "options"
                    clicked = True
                if quit_button.draw(screen) and clicked == False:
                    pygame.quit()
                    sys.exit()
                    clicked = True
                    # check if the options menu is open
            if menu_mode == "options":
                # draw the different options buttons
                if video_button.draw(screen) and clicked == False:
                    print("Video Settings")
                    clicked = True
                if audio_button.draw(screen) and clicked == False:
                    print("Audio Settings")
                    clicked = True
                if keys_button.draw(screen) and clicked == False:
                    print("Change Key Bindings")
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    menu_mode = "main"
                    clicked = True
        elif state == STARTSCREEN:
            screen.fill(BGCOLOUR)
            screen_text(TITLE, 48, WHITE, SCREEN_WIDTH / 2, screen_height / 4)
            screen_text("Arrows to move, Space to jump, ESCAPE to pause", 22, WHITE, SCREEN_WIDTH / 2, screen_height / 2)
            screen_text("Press any key to play", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4)
        elif state == ENDSCREEN:
            screen.fill(BGCOLOUR)
            screen_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, screen_height / 4)
            screen_text("Press any key to play again", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4)
        pygame.display.flip()

        clock.tick(60)
        continue

