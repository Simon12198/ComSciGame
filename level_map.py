from player import *
from csv_loader import *
tile_size = 32

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



class Level:
    def __init__(self, game_map, path, surface):
        self.game_map = game_map
        self.surface = surface
        self.game_map = self.load_map(path)

        self.tiles = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.terrain_layout = import_csv_files(self.game_map['Grass'])
        self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')

        self.Gold = import_csv_files(self.game_map['Gold'])
        self.create_sprite(self.Gold, 'Gold')

        self.trees = import_csv_files(self.game_map['Trees'])
        self.create_sprite(self.trees, 'Trees')

        self.spawn = import_csv_files(self.game_map['Spawn'])
        self.create_sprite(self.spawn, 'spawn')

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
        self.player = pygame.sprite.GroupSingle()
        row_index = 0
        for row in layout:
            col_index = 0
            for col in row:
                if col != '-1':
                    if type == 'Grass':
                        terrain_layout = slicing_tiles('data/graphics/Terrain/Grass/Grass.png')
                        tile = terrain_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32 , row_index * 32], tile)
                        self.tiles.add(sprite)
                    if type == 'Gold':
                        gold = slicing_tiles('data/graphics/Terrain/Coin/gold_coin.png')
                        tiles = gold[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiles)
                        self.coin.add(sprite)
                    if type == 'Trees':
                        trees = slicing_tiles('data/graphics/Terrain/Tree/Tree_0.png', (64,  64))
                        tiles = trees[0]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 29], tiles)
                        self.bg_objects.add(sprite)


                    if type == 'spawn':
                        player = Player([col_index * 32, row_index * 32])
                        self.player.add(player)
                col_index += 1

            row_index += 1
        self.tile_sprites = self.tiles.sprites()

    def scrolling(self):
        player = self.player.sprite
        true_scroll = [0, 0]
        true_scroll[0] += (player.rect.x-true_scroll[0] - rescaled_width  // 2 )/ 15
        true_scroll[1] += (player.rect.y - true_scroll[1] - rescaled_height // 2) / 15
        self.scroll = true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

    def collision_movement(self):
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
                self.coin.remove(coin)

        player.y = player.rect.y
        player.y += player.movement[1]
        player.rect.y = int(player.y)
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

    def button_released(self):
        player = self.player.sprite
        player.jump_held = False

    def change_key_bindings(self):
        if self.key_binding == "Normal" and keys_button.draw(screen):
            self.key_binding = "WASD"
        elif self.key_binding == "WASD" and keys_button.draw(screen):
            self.key_binding = "Normal"

    def run(self):
        # tiles
        self.scrolling()

        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)

        self.bg_objects.update(self.scroll)
        self.bg_objects.draw(self.surface)

        self.coin.update(self.scroll)
        self.coin.draw(self.surface)


        #player
        player = self.player.sprite
        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()





