import time, score
from player import *
from csv_loader import *
tile_size = 16

SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320



class Tiles(pygame.sprite.Sprite):
    def __init__(self, size, loc):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = loc)
    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

class ground_tile(Tiles):
    def __init__(self, size, loc, img):
        super().__init__(size, loc)
        self.image = img
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(img)



class Level:
    def __init__(self, game_map, path, surface, name, last_level = False):
        self.game_map = game_map
        self.surface = surface

        self.name = name
        self.path = path

        self.game_map = self.load_map(self.path)
        self.dead = False

        #used to calcuate final score
        self.final_score = True
        self.last_level = last_level

        #tile groups
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.Death = pygame.sprite.Group()
        self.Spawn = pygame.sprite.GroupSingle()
        self.End = pygame.sprite.Group()
        self.Tree = pygame.sprite.Group()
        self.slopesgroup = pygame.sprite.Group()
        self.topslopesgroup = pygame.sprite.Group()

        #use to calculate score
        self.score = 10000
        self.coin_count = 0
        self.start_time = time.time()


        self.terrain_layout = import_csv_files(self.game_map['Grass'])
        self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')

        self.Gold = import_csv_files(self.game_map['Gold'])
        self.create_sprite(self.Gold, 'Gold')

        self.spawn = import_csv_files(self.game_map['Spawn'])
        self.create_sprite(self.spawn, 'spawn')

        self.trees = import_csv_files(self.game_map['Trees'])
        self.create_sprite(self.trees, 'Trees')



        self.death = import_csv_files(self.game_map['Death'])
        self.create_sprite(self.death, 'death')

        self.slope = import_csv_files(self.game_map['Slopes'])
        self.slopes = self.create_sprite(self.slope, 'Slopes')



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
        return(level_data)

    def create_sprite(self, layout, type):
        row_index = 0
        for row in layout:
            col_index = 0
            for col in row:
                if col != '-1':
                    if type == 'Grass':
                        terrain_layout = slicing_tiles('data/graphics/Terrain/Grass/Grass.png')
                        tile = terrain_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 16 , row_index * 16], tile)
                        self.tiles.add(sprite)
                    if type == 'Slopes':
                        slope_layout = slicing_tiles('data/graphics/Terrain/Grass/Slope.png')
                        slope = slope_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 16, row_index * 16], slope)
                        self.slopesgroup.add(sprite)
                    if type == 'Gold':
                        gold = slicing_tiles('data/graphics/Terrain/Coin/gold_coin.png')
                        tiles = gold[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 16, row_index * 16], tiles)
                        self.coin.add(sprite)
                    if type == 'death':
                        death = slicing_tiles('data/graphics/Terrain/Death/Death.png')
                        tileset = death[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 16, row_index * 16], tileset)
                        self.Death.add(sprite)
                    if type == 'Trees':
                        if col == '0':
                            tree_0 = slicing_tiles('data/graphics/Terrain/Tree/Tree_0.png', (64, 64))
                            tree_set = tree_0[int(col)]
                            sprite = ground_tile(tile_size, (col_index * 16, (row_index - 3) * 16.1), tree_set)
                        if col == '1':
                            tree_1 = slicing_tiles('data/graphics/Terrain/Tree/Tree_1.png', (64, 64))
                            tree_1_set = tree_1[0]
                            sprite = ground_tile(tile_size, (col_index * 16, (row_index - 3) * 16.1), tree_1_set)
                        self.Tree.add(sprite)

                    if type == 'spawn':
                        life = slicing_tiles('data/graphics/Terrain/Spawn/Spawn.png')
                        born_set = life[int(col)]
                        if col == '0':
                            sprite = ground_tile(tile_size, [col_index * 16, row_index * 16], born_set)
                            if not(self.dead):
                                self.Spawn.add(sprite)
                            self.dead = True
                            player = Player([col_index * 16, row_index * 16])
                            self.player.add(player)
                            self.dead = False

                        if col == '1':
                            sprite = ground_tile(tile_size, [col_index * 16, row_index * 16], born_set)
                            self.End.add(sprite)


                col_index += 1
            row_index += 1
        self.tile_sprites = self.tiles.sprites()

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
            for coin in self.coin.sprites():
                if coin.rect.colliderect(player.rect):
                    self.coin_count += 1
                    self.coin.remove(coin)


            for death in self.Death.sprites():
                if death.rect.colliderect(player.rect):
                    self.dead = True
                    self.player.empty()


            player.y = player.rect.y
            player.y += player.movement[1]
            player.rect.y = int(player.y)

            maxVerticalOffset = 0  # in cases where player collides with multiple slopes at once, we should move him by maximum required amount, otherwise he'll be moved up next frame. Less jitter
            for slope in self.slopesgroup.sprites():
                if slope.rect.colliderect(player.rect):
                    offset = (slope.rect.left - player.rect.left, slope.rect.top - player.rect.top - 1)
                    almostCollisionOffset = player.mask.overlap(slope.mask,
                                                                offset)  # if not None: player is exactly 1 pixel above slope, aka touching the slope, without being inside of it
                    realCollisionOffset = pygame.sprite.collide_mask(player,
                                                                     slope)  # if not None: Player has at least 1 pixel inside the slope

                    if almostCollisionOffset:
                        self.collision_types['bottom'] = True  # remove vertical momentum

                    if realCollisionOffset:
                        verticalOffset = player.rect.height - realCollisionOffset[
                            1]  # move the player by this amount, and he'll be touching the current ground tile without being inside of it
                        if verticalOffset > maxVerticalOffset:
                            maxVerticalOffset = verticalOffset
                        self.collision_types['bottom'] = True
            if maxVerticalOffset:
                player.rect.bottom -= maxVerticalOffset

            maxtopVerticalOffset = 0
            for topslope in self.topslopesgroup.sprites():
                if topslope.rect.colliderect(player.rect):
                    topoffset = (topslope.rect.left - player.rect.left, topslope.rect.top - player.rect.top + 1)
                    almostCollisionOffset1 = player.mask.overlap(topslope.mask, topoffset)
                    realCollisionOffset2 = pygame.sprite.collide_mask(player, topslope)
                    if almostCollisionOffset1:
                        player.vertical_momentum = 0  # remove vertical momentum
                        player.collide_bottom = False
                    if realCollisionOffset2:
                        verticalOffset2 = player.rect.height + realCollisionOffset2[1]
                        if verticalOffset2 > maxtopVerticalOffset:
                            maxtopVerticalOffset = verticalOffset2
                            player.collide_bottom = False
            if maxtopVerticalOffset:
                player.rect.top += maxtopVerticalOffset

            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.movement[1] > 0:
                        player.rect.bottom = tile.rect.top
                        self.collision_types['bottom'] = True
                    if player.movement[1] < 0:
                        player.rect.top = tile.rect.bottom
                        self.collision_types['top'] = True


            for coin in self.coin.sprites():
                if coin.rect.colliderect(player.rect):
                    self.coin_count += 1
                    self.coin.remove(coin)
            if self.collision_types['bottom']:
                player.collide_bottom = True
                player.air_timer = 0
                player.vertical_momentum = 0
            else:
                player.collide_bottom = False
                player.air_timer += 1

            if self.collision_types['top']:
                player.vertical_momentum = 0
    def button_held(self):
        player = self.player.sprite
        player.jump_held = True

    def dying(self):
        self.player.empty()
        self.player = pygame.sprite.GroupSingle()
        if self.scroll[0] == 0 and self.scroll[1] == 0:
            player = Player([0, 0])
            self.player.add(player)
            self.dead = False
            print('YOU DIED')

    def button_released(self):
        player = self.player.sprite
        player.jump_held = False

    def end_level(self):
        if self.last_level:
            score.score_keeping(self.path, self.score, [self.coin_count, self.time_elasped, 0], self.name)
            self.final_score = True
        score.score_keeping(self.path, self.score, [self.coin_count, self.time_elasped, 0])

    def run(self):
        self.time_elasped = (time.time() - self.start_time)

        self.scrolling()

        #death
        if self.dead:
            self.dying()
        # tiles



        self.Tree.update(self.scroll)
        self.Tree.draw(self.surface)

        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)

        self.bg_objects.update(self.scroll)
        self.bg_objects.draw(self.surface)

        self.coin.update(self.scroll)
        self.coin.draw(self.surface)

        self.slopesgroup.update(self.scroll)
        self.slopesgroup.draw(self.surface)

        self.Death.update(self.scroll)

        self.Spawn.update(self.scroll)




        #player
        player = self.player.sprite

        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()
