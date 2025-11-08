import pgzrun
import random 

WIDTH = 640
HEIGHT = 480

# GAME CLASS #########################################################
class Game:
    def __init__(self):
        self.state = "MENU"

        self.ticks,self.delay = 0,0
        self.music,self.sounds = True, True

        self.play_button = Actor('menu/button_play')
        self.audio_button = Actor('menu/button_audio_on')
        self.music_button = Actor('menu/button_music_on')
        self.exit_button = Actor('menu/button_exit')

        self.play_button.x, self.play_button.y = 107,  350
        self.exit_button.x, self.exit_button.y = 107, 440
        self.audio_button.x, self.audio_button.y = 525, 350
        self.music_button.x, self.music_button.y = 525, 440

        sounds.menu_music.play(-1)

    def start(self):
        if self.state == "MENU":
            self.state = "NORMAL"
            sounds.menu_music.stop() 
            if self.music : sounds.music.play(-1)
            tileMap.setup()
            for key in enemies: 
                enemy = enemies[key]
                enemy.setup()
                player.setup()

    def stop(self):
        if self.state == "NORMAL":
            self.state = "MENU"
            sounds.music.stop()
            sounds.game_over.stop() 
            sounds.you_win.stop() 
            if self.music : sounds.menu_music.play(-1)

    def update(self):
            
        if self.ticks < 100:
            self.ticks += 1
        else:
            self.ticks = 0
 
        if self.delay > 0 : self.delay -= 1
    def draw(self):
        if self.state == "MENU":
            screen.blit('menu/menu',(0,0))

            audio_string, music_string = "menu/button_audio_","menu/button_music_"

            self.audio_button.image = audio_string + "on" if self.sounds else audio_string + "off"
            self.music_button.image = music_string + "on" if self.music else music_string + "off"

            self.play_button.draw(),self.audio_button.draw()
            self.music_button.draw(),self.exit_button.draw()

    def on_mouse_down(self,pos):
    
        if self.play_button.collidepoint(pos):
            self.start()

        if self.audio_button.collidepoint(pos):
            self.delay = 25
            
            if self.sounds:
                self.sounds = False 
                sounds.button.play()
            else:
                self.sounds = True 
                sounds.button.play()
        if self.music_button.collidepoint(pos):
            self.delay = 25
            if self.music:
                self.music = False 
                sounds.menu_music.stop()
                sounds.button.play()
            else:
                self.music = True 
                sounds.menu_music.play(-1)
                sounds.button.play()
        if game.exit_button.collidepoint(pos): pgzrun.sys.exit() 

######################################################################
# TILES CLASS ########################################################
class TileMap:
    def __init__(self):
        self.TILE_SIZE = 16
        self.DEFAULT_LINE = 'A00000000000000000000000000000000000000B'

        self.editable_map = [            
            'A00000000000000000000000000000000000000B',
            'A00000000000000000000000000000000000000B',
            'A000000000FFFFFFF0000FFFF0000FFFF00000GB',
            'A0000FF00099999990000999900009999000099B',
            'A00009900000000000000000000000000000000B',
	        'DFF000000000000000000000000000000000000B',
            'D78000000000000000000000000000000000000B',
            'DE2FF0000000000000000000000000000000000B',
            'D77780000000000000000000000000000000000B',
            'DDDE000322FFFFF223000000000000000000000B',
            'DDE000067780000677800000000000000000000B',
            'DE0000000000000000000032223000000000000B',
            'D00000000000000000000067778000000000000B',
            'A0000000000000000000000000000FFFFF445FFB',
            'A00000000000000000000000000006777777777D',
            'A2233FFFFF42FFFFFFF45FFFFFFF45CDDDDDDDDD',
            '1111111111111111111111111111111DDDDDDDDD',
         ]
        self.map = []
        self.walls = []
        self.collectables = []
        self.debug = False # Shows collision tiles
        self.FREE_SPACE = 30 - len(self.editable_map)

        for x in range(0,self.FREE_SPACE) : self.map.append(self.DEFAULT_LINE)
        for x in self.editable_map : self.map.append(x)

        self.tiles_solid = (
            "grass", "grass_left", "grass_right", "grass_middle", "dirt_left",
            "dirt_right", "block",
        )

        self.tile_collectables = ( "coins", "diamond" )
        self.tile_array = [
            "air", "grass","bush", "bush_small", "shrub_middle",
            "shrub_side", "grass_left", "grass_middle", 
            "grass_right", "block", "dirt_left", "dirt_right", 
            "mud_right", "mud_middle", "mud_left", "coins", "diamond"
        ]
        self.tile_dictionary = {
            '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, 
            '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9,
            'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13,
            'E' : 14, 'F' : 15, 'G' : 16, 'H' : 17,
            'I' : 18, 'J' : 19, 'K' : 20,
        }

        self.clouds = {}
        for i in range(0,25):
            self.clouds["cloud_" + str(i)] = (random.randrange(0,15),random.randrange(0,10),random.randrange(0,1))

        for y in range(0,len(self.map),1):
            for x in range(0, len(self.map[y]), 1):
                if len(self.map[y]) < 40 or len(self.map) < 30 : raise Exception("Linha de tiles insuficientes!")

                tile_line,tile_index,tile_name = self.get_tile_name(x,y)
                if tile_name in self.tiles_solid:

                    self.walls.append(Actor('tiles/collision_box', (x * self.TILE_SIZE + self.TILE_SIZE / 2,y * self.TILE_SIZE + self.TILE_SIZE / 2)))

        self.setup()
    def setup(self):
        self.collectables = []

        for y in range(0,len(self.map),1):
            for x in range(0, len(self.map[y]), 1):
                tile_line,tile_index,tile_name = self.get_tile_name(x,y)

                if tile_name in self.tile_collectables:
                    self.collectables.append(Actor('tiles/' + tile_name, (x * self.TILE_SIZE + self.TILE_SIZE / 2,y * self.TILE_SIZE + self.TILE_SIZE / 2)))

    def get_tile_name(self,x,y):
        tile_line = self.map[y] 
        tile_index = self.convert_tile(tile_line[x])
        tile_name = self.tile_array[tile_index]
        
        return tile_line,tile_index,tile_name
    
    def convert_tile(self,tile):
        return self.tile_dictionary[tile]
    
    def draw(self):
        
        for key in self.clouds:
            screen.blit("cloud_" + str(self.clouds[key][2]), (self.clouds[key][0] * 64,self.clouds[key][1] * 32))

        for y in range(len(self.map)):
            for x in range(0, len(self.map[y]), 1):

                tile_line,tile_index,tile_name = self.get_tile_name(x,y)

                if tile_name != "air" and tile_name not in self.tile_collectables: screen.blit("tiles/" + tile_name, (x * self.TILE_SIZE,y * self.TILE_SIZE))
        if self.debug: 
            for tile in self.walls: tile.draw()
        
        for tile in self.collectables:
            tile.draw()
######################################################################
# ENEMY CLASS ########################################################
class Enemy:
    def __init__(self, position,enemyType):
        self.actor = Actor("enemies/" + enemyType + "_right_0", position)
        self.start_x,self.start_y = position[0],position[1]

        self.enemy_type = enemyType
        self.setup()

    def setup(self):
        
        self.direction = "right"
        self.velocity = 1
        self.frame = 0
        self.actor.x, self.actor.y = self.start_x, self.start_y
        self.walk_limit,self.walk_limit_max = 0,0
        self.walkBack,self.isDead = False, False

        self.vertical_velocity = 0
        self.gravity = 0.3
        self.jump_strength = -5

        self.start_position = self.actor.x

        if self.enemy_type == "scorpion": 
            self.velocity = 1
            self.walk_limit_max = 32

        elif self.enemy_type == "bird": 
            self.velocity = 2
            self.walk_limit_max = 28

        elif self.enemy_type == "snake": 
            self.velocity = 1
            self.walk_limit_max = 64 + 32

    def update(self):
        if self.isDead:
            self.actor.y += self.vertical_velocity
            self.vertical_velocity += self.gravity
            if self.vertical_velocity > 10:
                self.vertical_velocity = 10  # cap fall speed

            return
        elif not self.isDead:
            self.vertical_velocity = 0

        if self.walk_limit >= self.walk_limit_max and not self.walkBack: self.walkBack = True

        if self.walk_limit <= 0 and self.walkBack: self.walkBack = False

        if self.walk_limit < self.walk_limit_max and not self.walkBack:
            self.direction = "right"
            self.actor.x += self.velocity
            self.walk_limit += 1
        
        if self.walk_limit > 0 and self.walkBack:
            self.direction = "left"
            self.actor.x -= self.velocity
            self.walk_limit -= 1
        
        if not self.isDead and self.actor.colliderect(player.actor):
            if player.isPunching: 
                self.isDead = True
                self.actor.angle = 180
                if game.sounds: sounds.hit.play()
                self.vertical_velocity = self.jump_strength

            if not player.isPunching: player.kill()
    def draw(self):
        actor_sprite = "enemies/" + self.enemy_type

        actor_sprite = actor_sprite + "_left_" if self.direction == "left" else actor_sprite + "_right_"
        
        if self.walk_limit % 10 == 0: self.frame += 1
        if self.frame > 1 : self.frame = 0

        if self.isDead: self.frame = 1

        if not self.isDead:
            self.actor.image = actor_sprite + str(self.frame)        

        self.actor.draw()

######################################################################

class Player:
    def __init__(self):
        self.actor = Actor('player/player_right_idle', (0,0))
        
        self.setup()
    def setup(self):

        self.direction = "right"
        self.velocity = 2
        self.vertical_velocity = 0
        self.gravity = 0.3
        self.jump_strength = -5

        self.won = False

        self.isDead,self.isMoving,self.isPunching,self.isJumping = False,False,False,False
        self.punch_timer, self.punch_delay = 0,25
        self.frame = 0
        self.actor.x = 2 * tileMap.TILE_SIZE
        self.actor.y = 28 * tileMap.TILE_SIZE
    
    def clamp_player(self):
        if self.actor.x < 0 or self.actor.x > 620: 
            self.actor.x = 2 * tileMap.TILE_SIZE
            self.actor.y = 28 * tileMap.TILE_SIZE
        elif self.actor.y > 500 or self.actor.y < 0:
            self.actor.x = 2 * tileMap.TILE_SIZE
            self.actor.y = 28 * tileMap.TILE_SIZE

    def update(self,keyboard):

        self.clamp_player()

        if self.isDead or self.won: return

        self.isMoving = False

        if keyboard.left:
            self.direction = "left"
            self.isMoving = True
        if keyboard.right:
            self.direction = "right"
            self.isMoving = True

        if self.isJumping:
            self.vertical_velocity += self.gravity
            if self.vertical_velocity > 10:
                self.vertical_velocity = 10  # cap fall speed
        else:
            self.vertical_velocity = 0

        if keyboard.space and not self.isJumping:
            self.vertical_velocity = self.jump_strength
            self.isJumping = True
            if game.sounds : sounds.jump.play()

        if keyboard.z and not self.isPunching and self.punch_delay <= 0:
            self.isPunching = True
            if game.sounds : sounds.punch.play()

        if self.punch_delay > 0: self.punch_delay -= 1

        if self.isPunching and self.punch_timer < 25: 
            self.punch_timer += 1
        elif self.isPunching  and self.punch_timer >= 25:
            self.isPunching = False
            self.punch_timer = 0
            self.punch_delay = 25
            
        self.move()
        self.check_ground()
    def move(self):
        horizontal_speed = -self.velocity if self.direction == "left" else self.velocity
        vertical_speed = self.vertical_velocity
        if self.isMoving:
            self.actor.x += horizontal_speed
            self.fix_position(horizontal_speed,0)
        if self.isJumping:  
            self.actor.y += vertical_speed
            self.fix_position(0,vertical_speed)
        

    def check_ground(self):
        self.actor.y += 1
        isJumping = any(self.actor.colliderect(tile) for tile in tileMap.walls)
        self.actor.y -= 1
        
        self.isJumping = not isJumping

    def fix_position(self,horizontalSpeed,verticalSpeed):
        for tile in tileMap.collectables:
            if self.actor.colliderect(tile):
                if tile.image == 'tiles/coins':
                    tile.x = 999
                    tile.y = 999
                    if game.sounds : sounds.coin.play()
                elif tile.image == 'tiles/diamond':
                    tile.x = 999
                    tile.y = 999
                    if game.sounds : sounds.coin.play()
                    player.win()
        for tile in tileMap.walls:
            if self.actor.colliderect(tile):

                if horizontalSpeed > 0: self.actor.right = tile.left;self.isMoving = False
                elif horizontalSpeed < 0:  self.actor.left = tile.right;self.isMoving = False

                elif verticalSpeed > 0:  # falling
                    self.actor.bottom = tile.top
                    self.vertical_velocity = 0
                    self.isJumping = False
                elif verticalSpeed < 0:  # jumping up
                    self.actor.top = tile.bottom
                    self.vertical_velocity = 0
    def draw(self):
        
        actor_direction = "player/player_left_" if self.direction == "left" else "player/player_right_" 
        
        if not self.isMoving: 
            self.frame = 0
            self.actor.image = actor_direction + "idle"
        
        if self.isMoving:
            if game.ticks % 5 == 0: self.frame += 1
            if self.frame > 3 : self.frame = 0

            self.actor.image = actor_direction + str(self.frame)
        if self.isJumping: self.actor.image = actor_direction + "jump"

        if self.isPunching: self.actor.image = actor_direction + "punch"

        if self.isDead: 
            self.actor.image = "player/player_dead"
            self.actor.draw()
            screen.blit("game_over", (0,0))     
        elif self.won:
            self.actor.image = "player/player_win"
            self.actor.draw()
            screen.blit("you_win", (0,0))     
        else:
            self.actor.draw()

    def win(self):
        if game.state == "NORMAL" and not self.isDead and not self.won:
            self.won = True
            sounds.music.stop()
            if game.music: sounds.you_win.play()
    def kill(self):
        if game.state == "NORMAL" and not self.isDead and not self.won:
            self.isDead = True
            sounds.music.stop()
            if game.music: sounds.game_over.play()

game = Game()
tileMap = TileMap()
player = Player()

anchor = tileMap.TILE_SIZE / 2
enemies = {
    "scorpion_1" : Enemy((24 * tileMap.TILE_SIZE + anchor,24 * tileMap.TILE_SIZE + anchor),"scorpion"),
    "scorpion_2" : Enemy((2 * tileMap.TILE_SIZE + anchor,20 * tileMap.TILE_SIZE + anchor),"scorpion"),
    "scorpion_3" : Enemy((34 * tileMap.TILE_SIZE + anchor,26 * tileMap.TILE_SIZE + anchor),"scorpion"),
    "snake_1" : Enemy((12 * tileMap.TILE_SIZE + anchor,28 * tileMap.TILE_SIZE + anchor),"snake"),
    "snake_2" : Enemy((21 * tileMap.TILE_SIZE + anchor,28 * tileMap.TILE_SIZE + anchor),"snake"),
    "snake_3" : Enemy((10 * tileMap.TILE_SIZE + anchor,15 * tileMap.TILE_SIZE + anchor),"snake"),
    "bird_1" : Enemy((11 * tileMap.TILE_SIZE + anchor,22 * tileMap.TILE_SIZE + anchor),"bird"),
    "bird_2" : Enemy((17 * tileMap.TILE_SIZE + anchor,15 * tileMap.TILE_SIZE + anchor),"bird"),
    "bird_3" : Enemy((25 * tileMap.TILE_SIZE + anchor,15 * tileMap.TILE_SIZE + anchor),"bird"),
    "bird_4" : Enemy((33 * tileMap.TILE_SIZE + anchor,15 * tileMap.TILE_SIZE + anchor),"bird"),
}
def update():
    game.update()

    if game.state == "NORMAL":
        if keyboard.escape:
            game.stop()
        for key in enemies: 
            enemy = enemies[key]
            enemy.update()
        player.update(keyboard)
def draw():
    screen.clear()
    screen.fill((0,170,255))
    
    game.draw()
    if game.state == "NORMAL":
        tileMap.draw()
        for key in enemies: 
            enemy = enemies[key]
            enemy.draw()
        player.draw()
        
def on_mouse_down(pos):
    if game.delay <= 0 and game.state == "MENU" : game.on_mouse_down(pos)  

pgzrun.go()