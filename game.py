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

in_game = True

users_message = []

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
    IMAGE = "Rock"
    SOLID = True
    RETURN = False

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True
    RETURN = False

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True
    RETURN = False

class Campanile(GameElement):
    IMAGE = "Campanile"
    SOLID = True
    RETURN = False

class StanfordTree(GameElement):
    IMAGE = "StanfordTree"
    SOLID = True
    RETURN = True

    def interact(self, player):
        GAME_BOARD.draw_msg("You touched the Stanford Tree! So you're stuck in prison until eternity...")

        next_x = 2
        next_y = 2

class Water(GameElement):
    IMAGE = "Water"
    SOLID = True
    RETURN = False

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    RETURN = False

    def interact(self, player):
        player.inventory["gold_key"] = self
        GAME_BOARD.draw_msg("You just acquired a key! You have %d item(s)!" %(len(player.inventory)))
        print player.inventory


class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    RETURN = False

    def interact(self, player):
        if "gold_key" in player.inventory:
            GAME_BOARD.del_el(door_closed.x, door_closed.y)
            GAME_BOARD.draw_msg("You've reached the Campanile, go rescue Princess %s!" % PRINCESS.IMAGE) 
        else:
            GAME_BOARD.draw_msg("You need a key to get into the Campanile. Maybe someone *cough Yoshua cough* has it. (Hint: The world always ends in two days.)")


class Character(GameElement):
    IMAGE = None
    SOLID = True

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

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

    def speak(self):
        GAME_BOARD.draw_msg("I am a character!")

class Player(Character):

    def __init__(self, image):
        GameElement.__init__(self)
        self.inventory = {}
        self.IMAGE = image

class Princess(Character):
    IMAGE = princess
    RETURN = False
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("Thank you for rescuing me %s! You win!!" % PLAYER.IMAGE) 

    def __init__(self, image):
        GameElement.__init__(self)
        self.inventory = {}
        self.IMAGE = image

class Yoshua(Character):
    IMAGE = "Yoshua"
    SOLID = True
    RETURN = False
    DEFEATED = False

    def interact(self, player):
        global users_message
        GAME_BOARD.draw_msg("'God's going to burn up this universe, sun, moon, and stars, and fold it up and burn it up.' You've just met Yoshua! Answer his riddle to move past him. 'How many days until the end of the world?'")
        
        if users_message == ['2']:
            global yoshua
            GAME_BOARD.del_el(yoshua.x, yoshua.y)
            gold_key = Key()
            GAME_BOARD.register(gold_key)
            GAME_BOARD.set_el(4, 3, gold_key)
            # GAME_BOARD.set_el(3, 3, yoshua2)
            GAME_BOARD.draw_msg("You got the answer! Here's a key to the Campanile. See you in Heaven!")
        # if yoshua2.DEFEATED:
        #     GAME_BOARD.draw_msg("You already took my key. Go away. 2 days.")
        # else:
        #     GAME_BOARD.draw_msg("'It's going to happen, it's going to happen, it happened on May 21, five months ago' Hm. That didn't work. Guess again.")


class Happy(Character):
    IMAGE = "Happy"
    SOLID = True
    RETURN = False

    def interact(self, player):
        global users_message
        GAME_BOARD.draw_msg("'Happy, happy, happy!' You've just met the Happy Happy Happy Man! Answer his riddle to move past him. 'Why did the chicken cross the road?' ")
        if users_message == ['h','a','p','p','y']:
            GAME_BOARD.del_el(happy.x, happy.y)
            happy2 = Happy()
            GAME_BOARD.register(happy2)
            GAME_BOARD.set_el(2, 6, happy2)
            GAME_BOARD.draw_msg("You got the answer! Come on through!")


class Oski(Character):
    IMAGE = "Oski"
    SOLID = True
    RETURN = False

    def interact(self, player):
        global users_message
        GAME_BOARD.draw_msg("*Silence* You've just met Oski! How will you get by? (a) Beat him in a staring contest (b) Distract him with candy (c) Give him a big bear hug")
        if users_message == ['a']:
            GAME_BOARD.draw_msg("Silly %s...you can't defeat Oski in a staring contest - he has no eyelids!!" % PLAYER.IMAGE)
        if users_message == ['b']:
            GAME_BOARD.draw_msg("Oh %s...Oski only eats organic, free-range, non-GMO candy. Try again." % PLAYER.IMAGE)
        if users_message == ['c']:
            GAME_BOARD.del_el(oski.x, oski.y)
            oski2 = Oski()
            GAME_BOARD.register(oski2)
            GAME_BOARD.set_el(11, 0, oski2)
            GAME_BOARD.draw_msg("Woohoo! Oski steps aside!")


####   End class definitions    ####

def in_game_keyboard_handler():
    direction = None
    if KEYBOARD[key.UP] and PLAYER.y != 0:
        direction = "up"
    if KEYBOARD[key.DOWN] and PLAYER.y != 9:
        direction = "down"
    if KEYBOARD[key.LEFT] and PLAYER.x != 0:
        direction  = "left"
    if KEYBOARD[key.RIGHT] and PLAYER.x != 14:
        direction = "right"
    for keypress in range(48,58):
        if KEYBOARD[keypress]:
            global users_message
            users_message += [chr(keypress)]
            GAME_BOARD.draw_msg(''.join(users_message))
    for keypress in range(97,123):
        if KEYBOARD[keypress]:
            global users_message
            users_message += [chr(keypress)]
            GAME_BOARD.draw_msg(''.join(users_message))
    if KEYBOARD[key.BACKSPACE]:
        if len(users_message) >= 1:
            users_message.pop()
            GAME_BOARD.draw_msg(''.join(users_message))

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
            GAME_BOARD.set_el(2, 2, PLAYER)
        elif existing_el is None or not existing_el.SOLID:
            # If there's nothing there _or_ if the existing element is not solid, walk through
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)


def initialize():
    """Put game initialization code here"""
    
    GAME_BOARD.draw_msg("%s is trapped in the Campanile. Defeat all the Berkeley characters to get the key to free %s!!!" % (princess, princess))
    
    print in_game
    
    in_game_keyboard_handler()

    # Initialize water
    water_positions = [
            (12,0),
            (12,2),
            (13,2),
            (14,2)
        ]

    for pos in water_positions:
        water = Water()
        GAME_BOARD.register(water) 
        GAME_BOARD.set_el(pos[0],pos[1],water)

    # Initialize tall trees
    talltree_positions = [
            (8,8),
            (11,4),
            (10,6),
            (12,8)
        ]

    for pos in talltree_positions:
        talltree = TallTree()
        GAME_BOARD.register(talltree) 
        GAME_BOARD.set_el(pos[0],pos[1],talltree)

    # Initialize walls
    wall_positions = [
            (0,5),
            (1,6),
            (3,8),
            (4,9)
        ]

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall) 
        GAME_BOARD.set_el(pos[0],pos[1],wall)

    # Initialize rocks
    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
        ]
    
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock) 
        GAME_BOARD.set_el(pos[0],pos[1],rock)

    # Initialize player
    global PLAYER
    PLAYER = Player(username)
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 9, PLAYER)
    print PLAYER

    # Initialize princess
    global PRINCESS
    PRINCESS = Princess(princess)
    GAME_BOARD.register(PRINCESS)
    GAME_BOARD.set_el(13, 0, PRINCESS)

    # Initialize Happy
    global happy
    happy = Happy()
    GAME_BOARD.register(happy)
    GAME_BOARD.set_el(2, 7, happy)

    # Initialize Yoshua
    global yoshua
    yoshua = Yoshua()
    GAME_BOARD.register(yoshua)
    GAME_BOARD.set_el(4, 3, yoshua)

    global yoshua2
    yoshua2 = Yoshua()
    yoshua2.DEFEATED = True
    GAME_BOARD.register(yoshua2)

    # Initialize Oski
    global oski
    oski = Oski()
    GAME_BOARD.register(oski)
    GAME_BOARD.set_el(11, 1, oski)

    # Initialize Stanford Tree
    stanfordtree = StanfordTree()
    GAME_BOARD.register(stanfordtree)
    GAME_BOARD.set_el(9, 5, stanfordtree)

    # Initialize campanile
    campanile = Campanile()
    GAME_BOARD.register(campanile)
    GAME_BOARD.set_el(14, 0, campanile)

    # Initialize door
    global door_closed
    door_closed = Door()
    GAME_BOARD.register(door_closed)
    GAME_BOARD.set_el(12, 1, door_closed)

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

# class Gem(GameElement):
#     IMAGE = "BlueGem"
#     SOLID = False
#     RETURN = False

#     def interact(self, player):
#         player.inventory.append(self)
#         GAME_BOARD.draw_msg("You just acquired a gem! You have %d item(s)!" %(len(player.inventory)))


# class Heart(GameElement):
#     IMAGE = "Heart"
#     SOLID = False
    # RETURN = False

    # def interact(self, player):
    #     player.inventory.append(self)
    #     GAME_BOARD.draw_msg("You just acquired a heart! You have %d item(s)!" %(len(player.inventory)))

    #     next_x = 2
    #     next_y = 2
