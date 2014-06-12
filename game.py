import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

username = raw_input("To choose a player type 'Aviva' or 'Katie': ")

if username == "Aviva":
    princess = "Katie"
else:
    princess = "Aviva"

print princess

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 15
GAME_HEIGHT = 10

#### Put class definitions here ####

class Rock(GameElement):
    IMAGE = princess
    SOLID = True
    RETURN = False

class Character(GameElement):
    IMAGE = None

    print dir(GameElement)

    def __init__(self, image):
        GameElement.__init__(self)
        self.inventory = []
        self.IMAGE = image

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False
    RETURN = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d item(s)!" %(len(player.inventory)))


class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    RETURN = True

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a heart! You have %d item(s)!" %(len(player.inventory)))

        next_x = 2
        next_y = 2

####   End class definitions    ####

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction  = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        # Check to see if there is an element already at those coordinates
        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is not None and existing_el.RETURN:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(2, 2, PLAYER)
        elif existing_el is None or not existing_el.SOLID:
            # If there's nothing there _or_ if the existing element is not solid, walk through
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


def initialize():
    """Put game initialization code here"""

    print princess

    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
        ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock) 
        GAME_BOARD.set_el(pos[0],pos[1],rock)
        rocks.append(rock)

    rocks[-1].SOLID = False 

    for rock in rocks:
        print rock

    GAME_BOARD.draw_msg("%s is trapped in the Campanile. Defeat all the Berkeley characters to get the key to free %s!!!" % (princess, princess))

    # Initialize player
    global PLAYER
    PLAYER = Character(username)
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    keyboard_handler()

    # Initialize gem
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    # Initialize heart
    heart = Heart()
    GAME_BOARD.register(heart)
    GAME_BOARD.set_el(0, 0, heart)



    # GAME_BOARD.erase_msg()



    # # Initialize and register rock 1
    # rock1 = Rock()
    # GAME_BOARD.register(rock1) # register rock with gameboard so it displays
    # GAME_BOARD.set_el(1,1,rock1) # places rock on gameboard at coordinates (1,1)

    # # Initialize and register rock 2
    # rock2 = Rock()
    # GAME_BOARD.register(rock2) 
    # GAME_BOARD.set_el(2,2,rock2) 

    # print "The first rock is at", (rock1.x, rock1.y)
    # print "The second rock is at", (rock2.x, rock2.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE

# def keyboard_handler():
#     if KEYBOARD[key.UP]:
#         GAME_BOARD.draw_msg("You pressed up")
#         next_y = PLAYER.y - 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
#     elif KEYBOARD[key.DOWN]:
#         GAME_BOARD.draw_msg("Down")
#         next_y = PLAYER.y + 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
#     elif KEYBOARD[key.LEFT]:
#         GAME_BOARD.draw_msg("To the left, to the left")
#         next_x = PLAYER.x - 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
#     elif KEYBOARD[key.RIGHT]:
#         GAME_BOARD.draw_msg("You're right!")
#         next_x = PLAYER.x + 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
#     elif KEYBOARD[key.SPACE]:
#         GAME_BOARD.erase_msg()
