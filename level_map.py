from player import *
tile_size = 20

SCREEN_WIDTH = 1200
screen_height = 576

rescaled_width = 600
rescaled_height = 288



class Tiles(pygame.sprite.Sprite):
    def __init__(self, loc, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = loc)



    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

class Level:
    def __init__(self, game_map, path, surface):
        self.game_map = game_map
        self.surface = surface
        self.game_map = self.load_map(path)
        self.render_tiles(self.game_map)
    def load_map(self, level_data):
        global screen_height
        f = open(level_data, 'r')
        self.level_data = f.read()
        f.close()
        self.level_data = self.level_data.split('\n')
        for row in self.level_data:
            screen_height += 1
            self.game_map.append(list(row))
        return self.game_map
    def render_tiles(self, game_map):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    tile = Tiles((x * tile_size, y * tile_size), tile_size)
                    self.tiles.add(tile)
                if tile == 'P':
                    player = Player((x * tile_size, y * tile_size))
                    self.player.add(player)
                x += 1
            y += 1
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

    def run(self):
        #tiles
        self.scrolling()
        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)

        #player
        player = self.player.sprite

        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()




