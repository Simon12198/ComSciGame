import pygame, sys  # import pygame and sys
import button
from level_map import Level
from pygame.locals import *
import math

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
audio_img = pygame.image.load('data/graphics/images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('data/graphics/images/button_keys.png').convert_alpha()
easter_egg_img = pygame.image.load('data/graphics/images/easteregg.png').convert_alpha()
back_img = pygame.image.load('data/graphics/images/button_back.png').convert_alpha()
logo_img = pygame.image.load('data/graphics/images/fatalecho (1).png').convert()
logo_img = pygame.transform.scale(logo_img, (SCREEN_WIDTH, screen_height))
mini_logo_img = pygame.image.load('data/graphics/images/logosmall.png').convert()
name_logo_img = pygame.image.load('data/graphics/images/namelogo.png').convert()
music_volume_img = pygame.image.load('data/graphics/images/music_volume.png').convert()
sfx_volume_img = pygame.image.load('data/graphics/images/sfx_volume.png').convert()
lower_volume_img = pygame.image.load('data/graphics/images/lower_volume.png').convert()
higher_volume_img = pygame.image.load('data/graphics/images/higher_volume.png').convert()
sword_icon_img = pygame.image.load('data/graphics/images/sword_icon.png').convert()
shield_icon_img = pygame.image.load('data/graphics/images/shield_icon.png').convert()
mushroom_trading_img = pygame.image.load('data/graphics/images/mushroom_trade.png').convert_alpha()
mushroom_trade_img = pygame.transform.scale(mushroom_trading_img, (400, 300))
buy_img = pygame.image.load('data/graphics/images/buy_button.png').convert_alpha()
sell_img = pygame.image.load('data/graphics/images/sell_button.png').convert_alpha()
plus_1_img = pygame.image.load('data/graphics/images/plus_1.png').convert_alpha()
coins_inv_img = pygame.image.load('data/graphics/images/coin_inv_img.png').convert_alpha()
coins_needed_img = pygame.image.load('data/graphics/images/coins_needed.png').convert_alpha()
mushroom_inv_img = pygame.image.load('data/graphics/images/mushroom_inv_img.png').convert_alpha()
mushroom_trade_bubble = pygame.image.load('data/graphics/images/mushroom_trade_bubble.png').convert_alpha()
armour_trade_bubble = pygame.image.load('data/graphics/images/armour_trade_bubble.png').convert_alpha()
mushroom_trade_bubble = pygame.transform.scale(mushroom_trade_bubble, (1200, 200))
armour_trade_bubble = pygame.transform.scale(armour_trade_bubble, (1200, 200))
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
buy_button = button.Button(SCREEN_WIDTH*1/2 - 40,screen_height * 1/4, buy_img, 1.2)
armour_button = button.Button(SCREEN_WIDTH /2 - 140, screen_height * 7/8 - 80, buy_img, 1.2)
weapons_button = button.Button(SCREEN_WIDTH /2 + 150, screen_height/2 + 140, buy_img, 1.2)
sell_button = button.Button(SCREEN_WIDTH*1/2 - 40,screen_height * 2/4, sell_img, 1.2)
sellmushrooms_button = button.Button(SCREEN_WIDTH*1/2 - 130,screen_height * 2/4 + 130, sell_img, 1.2)
quit_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 7/8, quit_img, 1.2)
audio_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 1/4 - 50, audio_img, 1.2)
keys_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 3/4 - 100, keys_img, 1.2)
merchant_back_button = button.Button(SCREEN_WIDTH*1/2 + 40,screen_height * 7/8 - 80, back_img, 1.2)
merchant_back1_button = button.Button(SCREEN_WIDTH*1/2 - 40,screen_height * 7/8 - 20, back_img, 1.2)
back_button = button.Button(SCREEN_WIDTH*1/2 - 100,screen_height * 7/8 - 50, back_img, 1.2)
mushroom_back_button = button.Button(SCREEN_WIDTH*1/2 + 50,screen_height * 2/4 + 130, back_img, 1.2)
back1_button = button.Button(SCREEN_WIDTH/2,screen_height/2, back_img, 1.2)
easter_egg_button = button.Button(SCREEN_WIDTH*1/2 - 200,screen_height * 1/5 - 100, easter_egg_img, 1)
sound_down_music_button = button.Button(SCREEN_WIDTH*1/2 + 200, screen_height * 1/5 + 100, lower_volume_img, 1)
sound_up_music_button = button.Button(SCREEN_WIDTH*1/2,screen_height * 1/5 + 100, higher_volume_img, 1)
sound_down_sound_button = button.Button(SCREEN_WIDTH*1/2 + 200, screen_height * 1/5 + 200, lower_volume_img, 1)
sound_up_sound_button = button.Button(SCREEN_WIDTH*1/2,screen_height * 1/5 + 200, higher_volume_img, 1)

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
cooldown = 750
screenswitch = pygame.USEREVENT + 0
finished_switch = pygame.USEREVENT + 1
attack = pygame.USEREVENT + 2
pygame.time.set_timer(finished_switch, time)
pygame.time.set_timer(screenswitch, time)

pygame.time.set_timer(attack, cooldown)
# Audio
pygame.mixer.init()

init_sfx_vol = 0.5
init_music_vol = 0.4
jump_sound = pygame.mixer.Sound("data/music/jump-sound.wav")
land_sound = pygame.mixer.Sound("data/music/land-sound.wav")
button_sound = pygame.mixer.Sound("data/music/menu_sound_effect.wav")
grass_walking_sound = pygame.mixer.Sound("data/music/grass-walking.wav")
menu_music = pygame.mixer.Sound("data/music/menu-music.wav")
pygame.mixer.music.load('data/music/music.wav')
pygame.mixer_music.play(-1, 0.0, 5000)
screen_change = False
main_music = 'unpaused'
merchant_mode = 'main'
merchant_collide = False
level = Level([], 'data/levels/level_3/', display, 'Eric')
RUNNING, PAUSE, TITLESCREEN, STARTSCREEN, ENDSCREEN, EASTEREGG, EEPAUSE, MERCHANT = 0, 1, 2, 3, 4, 5, 6, 7
state = TITLESCREEN
stop_drawing = False
merchant_speak = False
merchant_speak1 = False
merchant_sound = pygame.mixer.Sound("data/music/merchant_talking.wav")
merchant_sound.set_volume(0.2)
n = 1
while True:
    if level.done:
        level = Level([], f'data/levels/level_{n}/', display,  'Simon')
        n += 1
    for e in pygame.event.get():
        if e.type == attack:
            level.attack()
        if e.type == screenswitch:
            state = STARTSCREEN
        if e.type == finished_switch:
            screenswitch = 0
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_e and state == RUNNING:
                level.merchant_check()
                if level.merchant_check() == True:
                    state = MERCHANT
            if e.key == pygame.K_p and state == RUNNING:
                pygame.mixer.music.fadeout(2000)
            elif e.key == pygame.K_r and state == RUNNING:
                pygame.mixer.music.play(-1)
            if e.key == pygame.K_SPACE:
                if level.dead == False:
                    level.button_held()
                    jump_sound.play()
            if e.key == pygame.K_ESCAPE and state == RUNNING:
                state = PAUSE
            if e.key == pygame.K_ESCAPE and state == EASTEREGG:
                state = EEPAUSE
            if e.type == pygame.KEYUP:
                 if e.key == pygame.K_SPACE:
                     if level.dead == False:
                         level.button_released()
            if state == STARTSCREEN:
                if pygame.key.get_pressed():
                    state = RUNNING
        if e.type == pygame.MOUSEBUTTONUP:
            clicked = False

    else:
        if state == RUNNING:
            if main_music == 'paused':
                pygame.mixer_music.unpause()
                main_music = 'unpaused'
            level.draw_bg()
            level.run()
            level.draw_hearts()
            screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
            pygame.display.update()  # update the screen
        elif state == MERCHANT:
            #code for merchants, buttons and everything
            screen.fill('grey')
            if merchant_mode == "main":
                # draw pause screen buttons
                if buy_button.draw(screen) and clicked == False:
                    button_sound.play()
                    merchant_mode = 'buy'
                    clicked = True
                if sell_button.draw(screen) and clicked == False:
                    button_sound.play()
                    merchant_mode = 'sell'
                    clicked = True
                if merchant_back1_button.draw(screen) and clicked == False:
                    button_sound.play()
                    state = RUNNING
                    clicked = True
            if merchant_mode == "buy":
                # draw pause screen buttons
                coins = level.coin_inv
                merchantbuy_font = pygame.font.Font(None, 50)
                merchantbuy_surf = merchantbuy_font.render(str(coins), 1, (0, 0, 0))
                merchantbuy_pos = [SCREEN_WIDTH * 1 / 2 + 300, screen_height * 2 / 4]
                screen.blit(merchantbuy_surf, merchantbuy_pos)
                logo(shield_icon_img, rescaled_width / 2 + 200, rescaled_height /2 + 20)
                logo(coins_inv_img,SCREEN_WIDTH * 1 / 2 + 300, screen_height * 2 / 4 - 100)
                logo(coins_needed_img,SCREEN_WIDTH * 1 / 2 + 300, screen_height * 2 / 4 + 60)
                if armour_button.draw(screen) and clicked == False:
                    button_sound.play()
                    level.armour_trade(level.armour_trade_check())
                    clicked = True
                if merchant_back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    merchant_mode = 'main'
                    clicked = True
                if level.coin_counting(20):
                    logo(armour_trade_bubble, 1, screen_height / 2 - 320)
                    if merchant_speak == False:
                        merchant_sound.play()
                        merchant_speak = True
            if merchant_mode == "sell":
                merchant_speak1 = False
                # draw pause screen buttons
                mushrooms = level.mushroom_inv
                merchant_font = pygame.font.Font(None, 50)
                merchant_surf = merchant_font.render(str(mushrooms), 1, (0, 0, 0))
                merchant_pos = [SCREEN_WIDTH*1/2 + 300,screen_height * 2/4]
                screen.blit(merchant_surf, merchant_pos)
                logo(mushroom_trade_img,SCREEN_WIDTH*1/2 - 160,screen_height * 2/4 - 180)
                logo(mushroom_inv_img, SCREEN_WIDTH * 1 / 2 + 300, screen_height * 2 / 4 - 100)
                if sellmushrooms_button.draw(screen) and clicked == False:
                    button_sound.play()
                    level.mushroom_trade(level.mushroom_trade_check())
                    clicked = True
                if mushroom_back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    merchant_mode = 'main'
                    clicked = True
                if level.mushroom_count(1):
                    logo(mushroom_trade_bubble, 0, screen_height / 2 - 320)
                    if not merchant_speak1:
                        merchant_sound.play()
                        merchant_speak1 = True
        elif state == EASTEREGG:
            display.fill(LBLUE)
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
            if menu_mode == "main":
                # draw pause screen buttons
                if easter_egg_button.draw(screen) and clicked == False:
                    button_sound.play()
                    state = EASTEREGG
                    clicked = True
                if resume_button.draw(screen) and clicked == False:
                    button_sound.play()
                    state = RUNNING
                    clicked = True
                if options_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "options"
                    clicked = True
                if Levels_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "Levels"
                    clicked = True
                if quit_button.draw(screen) and clicked == False:
                    button_sound.play()
                    pygame.quit()
                    sys.exit()
                    clicked = True
                    # check if the options menu is open
            if menu_mode == "Levels":
                # draw the different options buttons
                if tutorial_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Tutorial")
                    clicked = True
                if Levels_1_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_1")
                    clicked = True
                if Levels_2_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_2")
                    clicked = True
                if Levels_3_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_3")
                    clicked = True
                if Levels_4_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_4")
                    clicked = True
                if back1_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "main"
                    clicked = True
            if menu_mode == "options":
                # draw the different options buttons
                if audio_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = 'audio settings'
                    clicked = True
                if keys_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("keybindings")
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "main"
                    clicked = True
            elif menu_mode == "audio settings":
                # draw the different options buttons
                logo(sfx_volume_img,SCREEN_WIDTH*1/2 - 400,screen_height * 1/5 + 200)
                logo(music_volume_img,SCREEN_WIDTH*1/2 - 400,screen_height * 1/5 + 100)
                audio_font = pygame.font.Font(None, 50)
                sfx_surf = audio_font.render(str(round(init_sfx_vol * 100)), 1, (0, 0, 0))
                sfx_pos = [SCREEN_WIDTH*1/2 + 100,screen_height * 1/5 + 200]
                music_surf = audio_font.render(str(round(init_music_vol * 100)), 1, (0, 0, 0))
                music_pos = [SCREEN_WIDTH * 1 / 2 + 100, screen_height * 1 / 5 + 100]
                screen.blit(sfx_surf, sfx_pos)
                screen.blit(music_surf, music_pos)

                if sound_up_music_button.draw(screen) and clicked == False and init_music_vol * 100 < 96:
                    button_sound.play()
                    init_music_vol += 0.0500
                    pygame.mixer.music.set_volume(init_music_vol)
                    clicked = True
                if sound_down_music_button.draw(screen) and clicked == False and init_music_vol * 100 >= 5:
                    button_sound.play()
                    init_music_vol -= 0.0500
                    pygame.mixer.music.set_volume(init_music_vol)
                    clicked = True
                if sound_up_sound_button.draw(screen) and clicked == False and init_sfx_vol * 100 < 96:
                    button_sound.play()
                    init_sfx_vol += 0.0500
                    button_sound.set_volume(init_sfx_vol)
                    jump_sound.set_volume(init_sfx_vol)
                    clicked = True
                if sound_down_sound_button.draw(screen) and clicked == False and init_sfx_vol * 100 >= 5:
                    button_sound.play()
                    init_sfx_vol -= 0.0500
                    button_sound.set_volume(init_sfx_vol)
                    jump_sound.set_volume(init_sfx_vol)
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "options"
                    clicked = True
        elif state == EEPAUSE:
            if main_music == 'unpaused':
                pygame.mixer_music.pause()
                main_music = 'paused'
            screen.fill(PURPLEBG)
            if menu_mode == "main":
                # draw pause screen buttons
                if easter_egg_button.draw(screen) and clicked == False:
                    button_sound.play()
                    state = RUNNING
                    clicked = True
                if resume_button.draw(screen) and clicked == False:
                    button_sound.play()
                    state = EASTEREGG
                    clicked = True
                if options_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "options"
                    clicked = True
                if Levels_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "Levels"
                    clicked = True
                if quit_button.draw(screen) and clicked == False:
                    button_sound.play()
                    pygame.quit()
                    sys.exit()
                    clicked = True
                    # check if the options menu is open
            if menu_mode == "Levels":
                # draw the different options buttons
                if tutorial_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Tutorial")
                    clicked = True
                if Levels_1_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_1")
                    clicked = True
                if Levels_2_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_2")
                    clicked = True
                if Levels_3_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_3")
                    clicked = True
                if Levels_4_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("Level_4")
                    clicked = True
                if back1_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "main"
                    clicked = True
            if menu_mode == "options":
                # draw the different options buttons
                if audio_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = 'audio settings'
                    clicked = True
                if keys_button.draw(screen) and clicked == False:
                    button_sound.play()
                    print("keybindings")
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "main"
                    clicked = True
            elif menu_mode == "audio settings":
                # draw the different options buttons
                logo(sfx_volume_img, SCREEN_WIDTH * 1 / 2 - 400, screen_height * 1 / 5 + 200)
                logo(music_volume_img, SCREEN_WIDTH * 1 / 2 - 400, screen_height * 1 / 5 + 100)
                audio_font = pygame.font.Font(None, 50)
                sfx_surf = audio_font.render(str(init_sfx_vol * 100), 1, (0, 0, 0))
                sfx_pos = [SCREEN_WIDTH * 1 / 2 + 100, screen_height * 1 / 5 + 200]
                music_surf = audio_font.render(str(init_music_vol * 100), 1, (0, 0, 0))
                music_pos = [SCREEN_WIDTH * 1 / 2 + 100, screen_height * 1 / 5 + 100]
                screen.blit(sfx_surf, sfx_pos)
                screen.blit(music_surf, music_pos)
                if sound_up_music_button.draw(screen) and clicked == False:
                    button_sound.play()
                    init_music_vol += 0.0500
                    clicked = True
                if sound_down_music_button.draw(screen) and clicked == False:
                    button_sound.play()
                    init_music_vol -= 0.0500
                    clicked = True
                if sound_up_sound_button.draw(screen) and clicked == False:
                    button_sound.play()
                    init_sfx_vol += 0.0500
                    clicked = True
                if sound_down_sound_button.draw(screen) and clicked == False:
                    button_sound.play()
                    init_sfx_vol -= 0.0500
                    clicked = True
                if back_button.draw(screen) and clicked == False:
                    button_sound.play()
                    menu_mode = "options"
                    clicked = True
        elif state == TITLESCREEN:
            logo(logo_img, 0, 0)
        elif state == STARTSCREEN:
            screen.fill(PURPLEBG)
            logo(mini_logo_img, rescaled_width / 2 + 35, 0)
            screen_text("Arrows to move, Space to jump, ESCAPE to pause, E to Interact with the Merchant", 22, WHITE, SCREEN_WIDTH / 2, screen_height / 2 + 50)
            screen_text("Press any key to play", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4 + 20)
        elif state == ENDSCREEN:
            screen.fill(BGCOLOUR)
            screen_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, screen_height / 4)
            screen_text("Press any key to play again", 22, WHITE, SCREEN_WIDTH / 2, screen_height * 3 / 4)
        pygame.display.flip()

        clock.tick(60)
        continue