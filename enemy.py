import pygame, sys
SCREEN_WIDTH = 1200
screen_height = 640
WINDOW_SIZE = (SCREEN_WIDTH, screen_height)  # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # initiate screen
from animation import load_animations

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.mush = []
        self.import_animation()
        self.frame = 0
        self.anim = self.animation_frames['idle']
        self.image = self.animations['idle'][self.anim[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0

    def import_animation(self):
        path = 'data/graphics/'
        self.animations = {'idle': []}
        animation_data = load_animations(path, 'mushroom')
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean
    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
        image = self.animations['idle'][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, self.flip, False)
    def update(self, scroll):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(True)
            if self.move_direction >= 0:
                self.flip_flip(False)
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.implement_anim(True)

class Imposter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.attack_animation = False
        self.import_animation()

        self.frame = 0
        self.action = ''
        self.change_action('idle')
        self.image = self.animations[self.action][self.anim[self.frame]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_action(self, new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.frame = 0
            self.anim = self.animation_frames[self.action]
    def import_animation(self):
        path = 'data/graphics/'
        self.animations = {'idle': [], 'attack': []}
        animation_data = load_animations(path, 'imposter')
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]
    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
            else:
                self.frame = 0
                break
        image = self.animations[self.action][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, False, False)
    def status(self):
        if self.attack_animation:
            self.change_action('attack')
        elif not(self.attack_animation):
            self.change_action('idle')

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.status()
        self.implement_anim(False)



class Swordsman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.import_animation()
        self.action = ''
        self.change_action('run')
        #swordsman attacking animation
        self.attack_animation = False
        self.current_frame = 0
        # swordsman running animation
        self.image = self.animations[self.action][self.anim[self.current_frame]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = False
        self.move_direction = 1
        self.move_counter = 0

    def change_flip(self, direction):
        if self.flip != direction:
            self.flip = direction


    def import_animation(self):
        path = 'data/graphics/'
        self.animations = {'idle': [], 'attack': [], 'run': []}
        animation_data = load_animations(path, 'swordsman')
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]

    def change_action(self, new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.frame = 0
            self.anim = self.animation_frames[self.action]

    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
            else:
                self.frame = 0
                break
        image = self.animations[self.action][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, self.flip, False)

    def status(self):
        if self.attack_animation:
            self.change_action('attack')
        elif not(self.attack_animation):
            self.change_action('run')

    def flip_flip(self, boolean):
        if self.flip != boolean:
            self.flip = boolean

    def move(self):
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
            if self.move_direction <= 0:
                self.flip_flip(False)
            if self.move_direction >= 0:
                self.flip_flip(True)
    def update(self, scroll):
        if self.action == 'run':
            self.rect.x += self.move_direction
            self.move()
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.status()
        self.implement_anim(True)
