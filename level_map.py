import time, score
import pygame.transform
from player import *
from csv_loader import *
import enemy

tile_size = 16

SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320
cooldown_tracker = 0
def logo(img, x, y):
    screen.blit(img, (x,y))

class Tiles(pygame.sprite.Sprite):
    def __init__(self, size, loc):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=loc)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]


class ground_tile(Tiles):
    def __init__(self, size, loc, img):
        super().__init__(size, loc)
        self.image = img
        self.mask = pygame.mask.from_surface(img)


class Level:
    def __init__(self, game_map, path, surface, name, last_level = False):
        self.game_map = game_map
        self.surface = surface
        self.name = name
        self.game_map = self.load_map(path)
        self.path = path
        self.bg_drawn = False
        self.player_direction = 0
        self.merchant_beside = 0
        self.mushroom_inv = 0
        self.mushroom_taken = 0 #for special ending if possible
        self.coin_inv = 0
        # used to calcuate final score
        self.final_score = True
        self.last_level = last_level
        self.damage = 10
        self.dead = False
        self.done = False
        self.health = 10
        self.max_health = 10
        self.damage_taken = False
        # heart images
        self.full_heart = pygame.image.load('data/graphics/bg_images/heart.png').convert_alpha()
        self.half_heart = pygame.image.load('data/graphics/bg_images/half_heart.png').convert_alpha()
        self.empty_heart = pygame.image.load('data/graphics/bg_images/empty_heart.png').convert_alpha()
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.imposter_group = pygame.sprite.Group()
        self.heart_objects = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.Death = pygame.sprite.Group()
        self.tree = pygame.sprite.Group()
        self.mushroom_group = pygame.sprite.Group()
        self.blob_group = pygame.sprite.Group()
        self.slopesgroup = pygame.sprite.Group()
        self.headslopesgroup = pygame.sprite.Group()
        self.swordsman_group = pygame.sprite.Group()
        self.merchant_group = pygame.sprite.Group()
        self.Spawn = pygame.sprite.GroupSingle()
        self.End = pygame.sprite.Group()
        self.merchant_speak = False
        self.merchant_speak1 = False
        # use to calculate score
        self.score = 10000
        self.coin_count = 0
        self.start_time = time.time()
        self.player_on_slope = False
        self.bg_imgs = []
        self.level_type = 'Eric'
        #background images added to list
        for i in range(1, 6):
            bg_img = pygame.image.load('data/graphics/bg_images/' + f'forest-{i}.png').convert_alpha()
            self.bg_imgs.append(bg_img)
        #creating and importing the game map files and sprites
        self.terrain_layout = import_csv_files(self.game_map['Grass'])
        self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')

        self.Gold = import_csv_files(self.game_map['Gold'])
        self.create_sprite(self.Gold, 'Gold')
        self.Mushroom = import_csv_files(self.game_map['Mushroom'])
        self.create_sprite(self.Mushroom, 'Mushroom')
        self.Swordsman = import_csv_files(self.game_map['Swordsman'])
        self.create_sprite(self.Swordsman, 'Swordsman')
        self.Imposter = import_csv_files(self.game_map['Imposter'])
        self.create_sprite(self.Imposter, 'Imposter')
        self.merchantslayout = import_csv_files(self.game_map['Merchant'])
        self.create_sprite(self.merchantslayout, 'Merchant')

        self.tree_layout = import_csv_files(self.game_map['Trees'])
        self.create_sprite(self.tree_layout, 'Trees')

        self.slope_layout = import_csv_files(self.game_map['Slopes'])
        self.slope_sprites = self.create_sprite(self.slope_layout, 'Slopes')

        self.headslope_layout = import_csv_files(self.game_map['TopSlopes'])
        self.headslope_sprites = self.create_sprite(self.headslope_layout, 'TopSlopes')

        self.spawn = import_csv_files(self.game_map['Spawn'])
        self.create_sprite(self.spawn, 'Spawn')

        self.death = import_csv_files(self.game_map['Death'])
        self.create_sprite(self.death, 'Death')


    def armour_trade_check(self):
        if self.coin_inv >= 5:
            return True
        else:
            return False

    def armour_trade(self, boolean):
        if boolean == True:
            self.coin_inv -= 20
            self.health += 1
            self.max_health += 1
        elif boolean == False:
            return True

    def mushroom_count(self, int):
        if self.mushroom_inv < int:
            return True
    def coin_counting(self, int):
        if self.coin_inv < int:
            return True
    def mushroom_trade_check(self):
        if self.mushroom_inv >= 1:
            return True
        else:
            return False


    def mushroom_trade(self, boolean):
        if boolean == True:
            self.mushroom_inv -= 1
            self.coin_inv += 5
        elif boolean == False:
            return True

    def load_map(self, path):
        level_data = {}
        f = open(path + 'level', 'r')
        self.level = f.read()
        f.close()
        self.level = self.level.split('\n')
        for name in self.level:
            paths = path.split('/')
            level_name = paths[2]
            level_data[name] = path + level_name + '_' + name + '.csv'
        return (level_data)
    def create_sprite(self, layout, type):
        global tile_size
        if self.path == 'data/levels/level_0':
            self.level_type = 'Eric'
            tile_size = 16
        elif 'level_3' in self.path:
            self.level_type = 'Simon'
            tile_size = 32
        row_index = 0
        for row in layout:
            col_index = 0
            for col in row:
                if col != '-1':
                    if type == 'Grass':
                        terrain_layout = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Grass/Grass.png', (tile_size, tile_size))
                        tile = terrain_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tile)
                        self.tiles.add(sprite)
                    if type == 'Gold':
                        gold = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Coin/gold_coin.png', (tile_size, tile_size))
                        tiles = gold[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tiles)
                        self.coin.add(sprite)
                    if type == 'Death':
                        death = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Death/Death.png', (tile_size, tile_size))
                        tileset = death[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tileset)
                        self.Death.add(sprite)
                    if type == 'Trees':
                        tree_layout = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Tree/Tree_tileset.png', (tile_size, tile_size))
                        tiled = tree_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tiled)
                        self.tree.add(sprite)
                    if type == 'Merchant':
                        tree_layout = slicing_tiles('data/graphics/images/merchant.png', (tile_size, tile_size))
                        tiled = tree_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        self.merchant_group.add(sprite)
                    if type == 'Mushroom':
                        mush_layout = slicing_tiles('data/graphics/mushroom/idle/idle_0.png', (16, 16))
                        tiled = mush_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tiled)
                        mushroom = enemy.Mushroom(col_index * tile_size, row_index * tile_size + 18)
                        self.mushroom_group.add(mushroom)
                    if type == 'Swordsman':
                        enemy_layout = slicing_tiles('data/graphics/images/swordsman.png', (tile_size, tile_size))
#                       tiled = enemy_layout[int(col)]
 #                      sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiled)
                        swordsman = enemy.Swordsman(col_index * tile_size, row_index * tile_size)
                        self.swordsman_group.add(swordsman)
                    if type == 'Imposter':
                        imposter_layout = slicing_tiles('data/graphics/images/imposter_tree.png', (tile_size, tile_size))
                        tiled = imposter_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], tiled)
                        imposter = enemy.Imposter(col_index * tile_size, row_index * tile_size - 32)
                        self.imposter_group.add(imposter)
                    if type == 'Slopes':
                        slope_layout = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Slopes/Slopes.png', (tile_size, tile_size))
                        ramps = slope_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], ramps)
                        self.slopesgroup.add(sprite)
                    if type == 'TopSlopes' and self.level_type == 'Simon':
                        slope_layout = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Slopes/Slopes.png', (tile_size, tile_size))
                        topramp = slope_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], topramp)
                        self.headslopesgroup.add(sprite)
                    if type == 'Spawn':
                        life = slicing_tiles(f'data/graphics/{self.level_type}Terrain/Spawn/Spawn.png', (tile_size, tile_size))
                        born_set = life[int(col)]
                        if col == '0':
                            sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], born_set)
                            if not self.dead:
                                self.Spawn.add(sprite)
                            self.dead = True
                            player = Player([col_index * tile_size, row_index * tile_size])
                            self.player.add(player)
                            self.dead = False
                        if col == '1':
                            sprite = ground_tile(tile_size, [col_index * tile_size, row_index * tile_size], born_set)
                            self.End.add(sprite)
                col_index += 1
            row_index += 1
        self.tile_sprites = self.tiles.sprites()
        self.slope_sprite = self.slopesgroup.sprites()
        self.headslope_sprites = self.headslopesgroup.sprites()

    def scrolling(self):
        spawn = self.Spawn.sprite
        player = self.player.sprite
        true_scroll = [0, 0]
        if self.dead == False:
            true_scroll[0] += (player.rect.x-true_scroll[0] - rescaled_width // 2) // 15
            true_scroll[1] += (player.rect.y-true_scroll[1] - rescaled_height // 2) // 15
            self.scroll = true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])
        else:
            true_scroll[0] += (spawn.rect.x-true_scroll[0])
            true_scroll[1] += (spawn.rect.y-true_scroll[1])
            self.scroll = true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])
    def collision_movement(self):
        if self.dead == False:
            player = self.player.sprite
            player.x = player.rect.x
            player.x += player.movement[0]
            player.rect.x = int(player.x)

            self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.movement[0] > 0:
                        player.rect.right = tile.rect.left
                        self.collision_types['right'] = True
                    if player.movement[0] < 0:
                        player.rect.left = tile.rect.right
                        self.collision_types['left'] = True

            player.y = player.rect.y
            player.y += player.movement[1]
            player.rect.y = int(player.y)

            self.slope_collision_from_above(player)
            self.slope_collision_from_below(player)
            self.rectangle_collision(player)
            self.mushroom_collision(player)
            self.merchant_collision(player)
            self.death_collision(player)
            self.coin_collision(player)
            self.end_collision(player)

            if self.collision_types['bottom']:
                player.collide_bottom = True
                player.air_timer = 0
                player.vertical_momentum = 0
            else:
                player.collide_bottom = False
                player.air_timer += 1

            if self.collision_types['top']:
                player.vertical_momentum = 0

    def rectangle_collision(self, player):
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.movement[1] > 0:
                    player.rect.bottom = tile.rect.top
                    self.collision_types['bottom'] = True
                if player.movement[1] < 0:
                    player.rect.top = tile.rect.bottom
                    self.collision_types['top'] = True

    def mushroom_collision(self, player):
        for mushroom in self.mushroom_group.sprites():
            mushroom_top = mushroom.rect.top
            player_bottom = player.rect.bottom
            if mushroom_top <= player_bottom:
                if mushroom.rect.colliderect(player.rect):
                    self.mushroom_group.remove(mushroom)
                    self.mushroom_inv += 1
                    self.mushroom_taken += 1

    def getFirstAndLastPointsOfCollision(self, collisionMask):
        firstPoint = None
        lastPoint = None
        for y_pos in range(collisionMask.get_size()[1]):
            for x_pos in range(collisionMask.get_size()[0]):
                position = (x_pos, y_pos)
                if collisionMask.get_at(position):
                    if not firstPoint:
                        firstPoint = position
                    lastPoint = position

        return firstPoint, lastPoint

    def slope_collision_from_below(self, player):
        maxtopVerticalOffset = 0

        for headslope in self.headslopesgroup.sprites():
            if headslope.rect.colliderect(player.rect):
                topoffset = (headslope.rect.left - player.rect.left, headslope.rect.top - player.rect.top + 1)

                collisionMask = player.mask.overlap_mask(headslope.mask, topoffset)
                firstIntersection, lastIntersection = self.getFirstAndLastPointsOfCollision(collisionMask)

                if firstIntersection:
                    verticalOffset = lastIntersection[1] - firstIntersection[1]
                    if verticalOffset > maxtopVerticalOffset:
                        maxtopVerticalOffset = verticalOffset

                if headslope.rect.right == player.rect.right:
                    player.rect.x += 1
                    player.rect.y += 1

                if headslope.rect.left == player.rect.left:
                    player.rect.x -= 1
                    player.rect.y += 1

        if maxtopVerticalOffset:
            player.rect.top += maxtopVerticalOffset

    def slope_collision_from_above(self, player):
        maxVerticalOffset = 0  # in cases where player collides with multiple slopes at once, we should move him by maximum required amount, otherwise he'll be moved up next frame. Less jitter
        for slope in self.slopesgroup.sprites():
            if slope.rect.colliderect(player.rect):
                offset = (slope.rect.left - player.rect.left, slope.rect.top - player.rect.top - 1)
                almostCollisionOffset = player.mask.overlap(slope.mask, offset)  # if not None: player is exactly 1 pixel above slope, aka touching the slope, without being inside of it
                realCollisionOffset = pygame.sprite.collide_mask(player, slope)  # if not None: Player has at least 1 pixel inside the slope
                if almostCollisionOffset:
                    if almostCollisionOffset[1] > slope.rect.height / 2:
                        self.collision_types['bottom'] = True  # remove vertical momentum

                        if realCollisionOffset:
                            verticalOffset = player.rect.height - realCollisionOffset[1]  # move the player by this amount, and he'll be touching the current ground tile without being inside of it
                            if verticalOffset > maxVerticalOffset:
                                maxVerticalOffset = verticalOffset

        if maxVerticalOffset:
            player.rect.bottom -= maxVerticalOffset

    def coin_collision(self, player):
        for coin in self.coin.sprites():
            if coin.rect.colliderect(player.rect):
                self.coin.remove(coin)
                self.coin_inv += 1
    def end_collision(self, player):
        for end_tile in self.End.sprites():
            if end_tile.rect.colliderect(player.rect):
                self.end_level()

    def merchant_collision(self, player):
        self.merchant_beside = 0
        for merchant in self.merchant_group.sprites():
            if merchant.rect.colliderect(player.rect):
                self.merchant_beside += 1

    def death_collision(self, player):
        for death in self.Death.sprites():
            if death.rect.colliderect(player.rect):
                self.dead = True
                self.health = 0
                self.player.empty()
    def attack(self):
        if self.dead == False:
            player = self.player.sprite
            player.x = player.rect.x
            player.x += player.movement[0]
            player.rect.x = int(player.x)
            self.direction = ''
            for imposter in self.imposter_group.sprites():
                imposter.attack_animation = False
                if imposter.rect.colliderect(player.rect):
                    imposter.attack_animation = True
                    self.health -= 4
            for swordsman in self.swordsman_group.sprites():
                swordsman.attack_animation = False
                if swordsman.rect.colliderect(player.rect):
                    swordsman.attack_animation = True
                    self.health -= 2
                    if player.rect.x > swordsman.rect.x:
                        swordsman.change_flip(True)
                        self.direction = 'left'
                    elif player.rect.x < swordsman.rect.x:
                        swordsman.change_flip(False)
                        self.direction = 'right'
                else:
                    if self.direction == 'left':
                        print('hello')
                        swordsman.change_flip(False)
                        self.direction = ''
                    elif self.direction == 'right':
                        swordsman.change_flip(True)
                        self.direction = ''



    def end_level(self):
        if self.last_level:
            score.score_keeping(self.path, self.score, [self.coin_count, self.time_elasped, 0], self.name)
            self.final_score = True
        score.score_keeping(self.path, self.score, [self.coin_count, self.time_elasped, 0])
        self.done = True
    def merchant_check(self):
        if self.merchant_beside != 0:
            return True
        else:
            return False


    def dying(self):
        self.player.empty()
        self.player = pygame.sprite.GroupSingle()
        if self.scroll[0] == 0 and self.scroll[1] == 0:
            player = Player((0, 0))
            self.player.add(player)
            self.health = 10
            self.dead = False
    def draw_img(self, img, x, y):
        self.surface.blit(img, (x, y))
    def draw_bg(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_RIGHT] and self.player_direction < 3000:
            self.player_direction += 1
        elif self.keys[pygame.K_LEFT] and self.player_direction > 0:
            self.player_direction -= 1
        for x in range(14):
            speed = 1
            for i in self.bg_imgs:
                self.surface.blit(i, ((x * 600) - self.player_direction * speed, 0))
                speed += 0.1
    def draw_hearts(self):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0
        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                self.surface.blit(self.full_heart, (heart * 30 + 5, 10))
            elif half_heart_exists and int(half_hearts_total) == heart:
                self.surface.blit(self.half_heart, (heart * 30 + 5, 10))
            else:
                self.surface.blit(self.empty_heart, (heart * 30 + 5, 10))
        if self.health <= 0:
            self.dead = True
    def button_held(self):
        player = self.player.sprite
        player.jump_held = True

    def button_released(self):
        player = self.player.sprite
        player.jump_held = False
    def run(self):
        # tiles
        self.time_elasped = (time.time() - self.start_time) * 50
        self.scrolling()
        # death
        if self.dead:
            self.dying()
        # merchant check
        self.merchant_check()
        #background drawing
        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)
        self.slopesgroup.update(self.scroll)
        self.slopesgroup.draw(self.surface)
        self.headslopesgroup.update(self.scroll)
        self.headslopesgroup.draw(self.surface)
        self.mushroom_group.update(self.scroll)
        self.mushroom_group.draw(self.surface)
        self.imposter_group.update(self.scroll)
        self.imposter_group.draw(self.surface)

        self.End.update(self.scroll)
        self.bg_objects.update(self.scroll)
        self.bg_objects.draw(self.surface)
        self.heart_objects.draw(self.surface)
        self.coin.update(self.scroll)
        self.coin.draw(self.surface)
        self.tree.update(self.scroll)
        self.tree.draw(self.surface)
        self.blob_group.update(self.scroll)
        self.blob_group.draw(self.surface)
        self.swordsman_group.update(self.scroll)
        self.swordsman_group.draw(self.surface)
        self.Death.update(self.scroll)
        self.Spawn.update(self.scroll)
        self.merchant_group.update(self.scroll)
        self.merchant_group.draw(self.surface)
        # player
        player = self.player.sprite

        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()


