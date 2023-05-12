import pygame, sys  # import pygame and sys
import button
from level_map import Level
pygame.init()  # initiate pygame
clock = pygame.time.Clock()  # set up the clock
pygame.display.set_caption('Fatal Echo')  # set the window name
SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320

WINDOW_SIZE = (SCREEN_WIDTH, screen_height)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # initiate screen

display = pygame.Surface((rescaled_width, rescaled_height))
# define colours
TEXT_COL = (255, 255, 255)
WHITE = (255, 255, 255)
BGCOLOUR = (0, 128, 255)
PURPLEBG = (85, 0, 149)
LBLUE = (0, 163, 233)

# load button images
levels_img = pygame.image.load("data/graphics/images/button_levels.png").convert_alpha()
tutorial_img = pygame.image.load("data/graphics/images/button_tutorial.png").convert_alpha()
Level1_img = pygame.image.load("data/graphics/images/button_level_1.png").convert_alpha()
Level2_img = pygame.image.load("data/graphics/images/button_level_2.png").convert_alpha()
Level3_img = pygame.image.load("data/graphics/images/button_level_3.png").convert_alpha()
Level4_img = pygame.image.load("data/graphics/images/button_level_4.png").convert_alpha()
resume_img = pygame.image.load("data/graphics/images/button_resume.png").convert_alpha()
options_img = pygame.image.load("data/graphics/images/button_options.png").convert_alpha()
quit_img = pygame.image.load("data/graphics/images/button_quit.png").convert_alpha()
video_img = pygame.image.load('data/graphics/images/button_video.png').convert_alpha()
audio_img = pygame.image.load('data/graphics/images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('data/graphics/images/button_keys.png').convert_alpha()
easter_egg_img = pygame.image.load('data/graphics/images/easteregg.png').convert_alpha()
back_img = pygame.image.load('data/graphics/images/button_back.png').convert_alpha()
logo_img = pygame.image.load('data/graphics/images/fatalecho (1).png').convert()
mini_logo_img = pygame.image.load('data/graphics/images/logosmall.png').convert()
name_logo_img = pygame.image.load('data/graphics/images/namelogo.png').convert()

# create button instances
#to remember order of function:
#(self, x, y, image, scale)
Levels_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 3/4 - 30, levels_img, 1)
tutorial_button = button.Button(SCREEN_WIDTH*1/2 - 400,screen_height * 1/4 - 100, tutorial_img, 1)
Levels_1_button = button.Button(SCREEN_WIDTH*1/2 + 200,screen_height * 1/4 - 100, Level1_img, 1)
Levels_2_button = button.Button(SCREEN_WIDTH*1/2 - 400,screen_height * 2/4 - 100, Level2_img, 1)
Levels_3_button = button.Button(SCREEN_WIDTH*1/2 + 200,screen_height * 2/4 - 100, Level3_img, 1)
Levels_4_button = button.Button(SCREEN_WIDTH*1/2 - 400,screen_height * 7/8 - 100, Level4_img, 1)
resume_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 1/4, resume_img, 1.2)
options_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 2/4, options_img, 1.2)
quit_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 7/8, quit_img, 1.2)
video_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 1/4 - 100, video_img, 1.2)
audio_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 2/4 - 100, audio_img, 1.2)
keys_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 3/4 - 100, keys_img, 1.2)
back_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 7/8 - 50, back_img, 1.2)
back1_button = button.Button(SCREEN_WIDTH/2,screen_height/2, back_img, 1.2)
easter_egg_button = button.Button(SCREEN_WIDTH*1/2 - 200,screen_height * 1/5 - 100, easter_egg_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def screen_text(text, fontsize, color, x, y):
    font = pygame.font.SysFont("arial", fontsize)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
def logo(img, x, y):
    screen.blit(img, (x,y))
menu_mode = "main"
clicked = False
time = 3500
screenswitch = pygame.USEREVENT + 0
finished_switch = pygame.USEREVENT + 1
pygame.time.set_timer(finished_switch, time)
pygame.time.set_timer(screenswitch, time)
jump_sound = pygame.mixer.Sound('data/music/jump.wav')
grass_walking_sound = pygame.mixer.Sound('data/music/grass-walking.wav')
menu_music = pygame.mixer.Sound('data/music/menu-music.wav')
pygame.mixer.music.load('data/music/music.wav')
pygame.mixer_music.play(-1)
main_music = 'unpaused'
level = Level([], 'data/levels/level_3/', display)
RUNNING, PAUSE, TITLESCREEN, STARTSCREEN, ENDSCREEN, EASTEREGG, EEPAUSE = 0, 1, 2, 3, 4, 5, 6
state = TITLESCREEN
while True:
    for e in pygame.event.get():
        if e.type == screenswitch:
            state = STARTSCREEN
        if e.type == finished_switch:
            screenswitch = 0
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p and state == RUNNING:
                pygame.mixer.music.fadeout(2000)
            elif e.key == pygame.K_r and state == RUNNING:
                pygame.mixer.music.play(-1)
            if e.key == pygame.K_SPACE:
                level.button_held()
            if e.key == pygame.K_ESCAPE and state == RUNNING:
                state = PAUSE
            if e.key == pygame.K_ESCAPE and state == EASTEREGG:
                state = EEPAUSE
            if e.type == pygame.KEYUP:
                 if e.key == pygame.K_SPACE:
                    level.button_released()
            if state == STARTSCREEN:
                if pygame.key.get_pressed():
                    state = RUNNING
        if e.type == pygame.MOUSEBUTTONUP:
            clicked = False

    else:
        if state == RUNNING:
            pygame.mixer.Sound.stop(menu_music)
            if main_music == 'paused':
                pygame.mixer_music.unpause()
                main_music = 'unpaused'
            level.draw_bg()
            level.run()
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()  # update the screen
        if state == EASTEREGG:
            display.fill(LBLUE)
            pygame.mixer.Sound.stop(menu_music)
            if main_music == 'paused':
                pygame.mixer_music.unpause()
                main_music = 'unpaused'
            level.run()
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()  # update the screen
        elif state == PAUSE:
            screen.fill(PURPLEBG)
            if main_music == 'unpaused':
                pygame.mixer_music.pause()
                main_music = 'paused'
            pygame.mixer.Sound.play(menu_music)
            if menu_mode == "main":
                # draw pause screen buttons
                if easter_egg_button.draw(screen) and clicked == False:
                    state = EASTEREGG
                    clicked = True
                if resume_button.draw(screen) and clicked == False:
                    state = RUNNING
                    clicked = True
                if options_button.draw(screen) and clicked == False:
                    menu_mode = "options"
                    clicked = True
                if Levels_button.draw(screen) and clicked == False:
                    menu_mode = "Levels"
                    clicked = True
                if quit_button.draw(screen) and clicked == False:
                    pygame.quit()
                    sys.exit()
                    clicked = True
                    # check if the options menu is open
            if menu_mode == "Levels":
                # draw the different options buttons
                if tutorial_button.draw(screen) and clicked == False:
                    print("Tutorial")
                    clicked = True
                if Levels_1_button.draw(screen) and clicked == False:
                    print("Level_1")
                    clicked = True
                if Levels_2_button.draw(screen) and clicked == False:
                    print("Level_2")
                    clicked = True
                if Levels_3_button.draw(screen) and clicked == False:
                    print("Level_3")
                    clicked = True
                if Levels_4_button.draw(screen) and clicked == False:
                    print("Level_4")
                    clicked = True
                if back1_button.draw(screen) and clicked == False:
                    menu_mode = "main"
                    clicked = True
            if menu_mode == "options":
                # draw the different options buttons
                if video_button.draw(screen) and clicked == False:
                    print("Video Settings")
                    clicked = True
                if audio_button.draw(screen) and clicked == False:
                    print("Audio Settings")
                    clicked = True
                if keys_button.draw(screen) and clicked == False:
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    menu_mode = "main"
                    clicked = True
        elif state == EEPAUSE:
            if main_music == 'unpaused':
                pygame.mixer_music.pause()
                main_music = 'paused'
            pygame.mixer.Sound.play(menu_music)
            screen.fill(PURPLEBG)
            if menu_mode == "main":
                # draw pause screen buttons
                if easter_egg_button.draw(screen) and clicked == False:
                    state = RUNNING
                    clicked = True
                if resume_button.draw(screen) and clicked == False:
                    state = EASTEREGG
                    clicked = True
                if options_button.draw(screen) and clicked == False:
                    menu_mode = "options"
                    clicked = True
                if Levels_button.draw(screen) and clicked == False:
                    menu_mode = "Levels"
                    clicked = True
                if quit_button.draw(screen) and clicked == False:
                    pygame.quit()
                    sys.exit()
                    clicked = True
                    # check if the options/levels menu is open
            if menu_mode == "Levels":
                # draw the different options buttons
                if tutorial_button.draw(screen) and clicked == False:
                    print("Tutorial")
                    clicked = True
                if Levels_1_button.draw(screen) and clicked == False:
                    print("Level_1")
                    clicked = True
                if Levels_2_button.draw(screen) and clicked == False:
                    print("Level_2")
                    clicked = True
                if Levels_3_button.draw(screen) and clicked == False:
                    print("Level_3")
                    clicked = True
                if Levels_4_button.draw(screen) and clicked == False:
                    print("Level_4")
                    clicked = True
                if back1_button.draw(screen) and clicked == False:
                    menu_mode = "main"
                    clicked = True
            if menu_mode == "options":
                # draw the different options buttons
                if video_button.draw(screen) and clicked == False:
                    print("Video Settings")
                    clicked = True
                if audio_button.draw(screen) and clicked == False:
                    print("Audio Settings")
                    clicked = True
                if keys_button.draw(screen) and clicked == False:
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    menu_mode = "main"
                    clicked = True
        elif state == TITLESCREEN:
            logo(logo_img, 0, 0)
        elif state == STARTSCREEN:
            screen.fill(PURPLEBG)
            logo(mini_logo_img, rescaled_width / 2 + 35, 0)
            screen_text("Arrows to move, Space to jump, ESCAPE to pause", 22, WHITE, SCREEN_WIDTH / 2, screen_height / 2 + 50)
            screen_text("Press any key to play", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4 + 20)
        elif state == ENDSCREEN:
            screen.fill(BGCOLOUR)
            screen_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, screen_height / 4)
            screen_text("Press any key to play again", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4)
        pygame.display.flip()

        clock.tick(60)
        continue