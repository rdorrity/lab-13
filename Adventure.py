# Team SCSI Logic
# Sara Kazemi, Ryan Dorrity
# Lab 13
# 12/3/2018
# ###########################################################

# TESTED IN PYTHON 3.7
# Welcome to Stargate: SCSI-1! A Text Based Adventure

# To win, go to the north room and take the key
# go back south to the main room
# go south and examine the socket and you will
# enter the secret room!
# In the secret room, take the logic board
# You will wind up back in the main room
# Go east and take the necklace
# Head back west to the main room
# Go west to the west room
# Examine the gyroscope to win!

# To LOSE, do everything above, except you will also
# take the book in the in the east room, which adds
# a "tablet" to your inventory
# When you examine the gyroscope in the west room,
# You will get the bad ending.

# You can also get a losing condition by talking to
# the chair in the north room.


# Game Map:
#
#                     --------------------
#                    |                    |
#                    |                    |
#                    |                    |
#                    |     NORTH ROOM     |
#                    |                    |
#                    |                    |
#                    |                    |
# ----------------------------DOOR --------------------------
# |                  |                    |                  |
# |                  |                    |                  |
# |                  |                    |                  |
# |                  D                    D                  |
# |   WEST ROOM      O      START         O   EAST ROOM      |
# |                  O                    O                  |
# |                  R                    R                  |
# |                  |                    |                  |
#  ---------------------------DOOR --------------------------
#                    |                    |
#                    |                    |
#                    |                    |
#                    |                    |
#                    |    SOUTH ROOM      |
#                    |                    |
#                    |                    |
#                    |                    |
#                    |                    |
#                     --------------------
#

import re

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


root = tk.Tk()
window = tk.Canvas(root, width=100, height=100)
def game_init():

    button = tk.Button(window, text="Start Adventure", command=go)
    button2 = tk.Button(window, text="Quit", command=quit)
    window.pack()
    button.pack()
    button2.pack()
    window.mainloop()




# The location class initializes all rooms in the game world.
# Each Location has:
# String: name (prints when you visit a room)
# String: description (prints the first time you visit a room or of you "look" at a room).
# Dictionary: connections (keys are Strings that refer to a valid direction a character can move from this Location
# and the values are reference variables of the rooms corresponding to those directions.
# boolean: visited: Initialized to False and changes to True once the player moves to a new room.
class Location:
    # Constructor for our locations.
    def __init__(self, name, description, connections):
        self.name = name
        self.description = description
        self.connections = connections
        self.visited = False

    def print_description(self):
        print("\n\t~~" + self.name + "~~\n")
        if not self.visited:    # Only print the description of the room if Player hasn't been there before
                                # Note: Player can use "look" to see the description again
            print(self.description)

    def remove_item(self, item):
        if item in itemTable:   # When an item is removed from the room, we should remove its description
                                # from our itemTable and replace it with an empty string.
                                # This removes the item description from the room's description.
            self.description = self.description.replace(itemTable[item][2], "")

    def __getitem__(self):      # helper function. Not really used at the moment. Remove?
        return self.name


# Room Definitions
# Rooms are created ahead of time with empty values because we need to refer to these objects in their
# connections dictionary.
main_room = Location("", "", {})
north_room = Location("", "",  {})
south_room = Location("", "",  {})
east_room = Location("", "",  {})
west_room = Location("", "",  {})
secret_room = Location("", "",  {})

# World Items
# A dictionary that holds all the items in the world as keys. The values are lists.
# The 0th index of that list holds the description of the item when the Player examines the item
# The 1st index of the list holds the reference object (a Location or Player) that possesses the item
# The 2nd index of the list holds the description of the item that gets concatenated to the room's location\
# The 3rd index of the list is a boolean checking if an item at a location is retrievable by the player, if true.
# This description turns into the empty string when a player takes the item.
itemTable = {
 "letter": ["\n\tMy brave Elana,\n\nI need you to find this. I need you to know before I'm gone.\n\n\
 My ambition was fueled only by my love for you. I had to have more time.\n\
 More time to traverse the Celestial Ocean you love so much.\n\
 The irony of my fate is not lost on me.\n\
 I hope you will forgive my foolishness and know that,\n\
 no matter where...or when I may be, my love for you will be there.\n\n\
 Do not follow. Your existence belongs in the stars.\n\n\
 For all eternity,\n\n\
 \t-Trelle", east_room, "\nA letter, crumbled and scribbled, lies to the side.", True],
 "key": ["\nThe rust appears light, but scrapes on the surface appear deep.\n", north_room, "\nA rusted key sits on a side table.", True],
 "logic board": ["\nSpeckled with strange connectors and black squares.\n", secret_room, "\nYou see a dusty green board on the ground.", True],
 "necklace": ["\nStaring into the pendant, your sense of time dissolves.\n", east_room, "\nIn the center of the table rests a silver necklace, its pendant pure crystal.", True],
 "book": ["\nThe black hand print on the cover pulls at your thoughts with hunger.\n", south_room, "\nThere is a tattered book on a lectern.", True],
 "chair" : ["This space purposely left empty.", north_room, "\nBy the fire, a chair sits with a surprising allure.", False],
 "tablet" : ["\nBlack as the void, the stone feels moist in your grip.\nThere are electrical connectors on one side.\n", None, "This space purposely left empty.", True],
 "gyroscope" : ["\nSilver metal with brass filigree.\
 \nA panel shows slots for multiple instruments.\
 \nTwo are empty. One looks rough and angular.\
 \nThe other has straight edges and places for connectors.\n", west_room, "This space purposely left empty.", False],
 "socket" : ["\nPeering inside the socket, you see metallic pins.", south_room, "This space purposely left empty.", False]
}

# Room Initializations

# Main Room
main_room.name = "Main Room"
main_room.description = "Lit with a flickering torchlight, the room darkens at the corners. \
The walls are\nCyclopean stone and painted with moss. \
Motes of flora drift lightly and your feet\nsettle on soft grass. \
Four doors face you in each cardinal direction.\n"
main_room.connections = {"north": north_room, "south": south_room,
                         "east": east_room, "west": west_room}

# North Room
north_room.name = "North Room"
north_room.description = "The warmth of the room sends shivers down your back,\n\
like settling into a warm bath in winter.\n\
A fireplace burns to the side, inviting and bright,\n\
while a grandfather clock creates meditative ticking from a corner." + itemTable["key"][2] + itemTable["chair"][2] + "\nThe only door is to the south.\n"
north_room.connections = {"south": main_room}

# South Room
south_room.name = "South Room"
south_room.description = "The grass from the prior room gives way to soil.\n\
A small spring begins near the north and disappears into the far stone wall.\n\
Worn tables are covered with failed inventions and stagnate chemical devices.\n\
A rough mosaic colors one wall, forming the shapes of two women sailing through a strange sea.\n\
Amongst the waves you discover a small socket." + itemTable["book"][2] + "\nThere's a door to the north.\n"
south_room.connections = {"north": main_room}

# East Room
east_room.name = "East Room"
east_room.description = "Stepping onto a stone floor, you strain to see in the dim light.\n\
Rows of portraits line the walls, depicting strange, archaic scenes of battle.\n\
The air is spiced with a sweet perfume that pulls you inward and you fail to resist.\n\
You collide with a stone table that breaks the hold on your mind." + itemTable["letter"][2] + itemTable["necklace"][2] + "\nA doorway is to the west.\n"
east_room.connections = {"west": main_room}

# West Room
west_room.name = "West Room"
west_room.description = "Built-in shelves cover three of the walls,\n\
housing books and strange scientific instruments.\n\
Pages are scattered on the polished wood floor, the written words no longer legible.\n\
The far wall is made entirely of glass and an endless night sky rests on the other side.\n\
In the center of the room is a large device, a gyroscope, rotating slow and steady.\n"
west_room.connections = {"east": main_room}

# Secret Room
secret_room.name = "Secret Room"
secret_room.description = "Descending stone steps, you enter a chamber of white stone.\n\
Every surface is smooth and cold to the touch.\n\
The stream from above falls and clings to one wall, but there is no sound.\n\
Your footsteps are silent, and shouting creates no sound.\n\
The doorway you entered from is gone, but you notice a dusty green board beneath your feet.\n\
It resembles a logic board.\n"
secret_room.connections = {}

# Ending Scripts.
# BAD Ending occurs if you examine the gyroscope in the west room and you have the necklace and the tablet
# OR if you have the necklace, tablet, and logic board
badEnding = "\nPlacing the pendant and tablet into the panel, you begin to feel vibrations deep below.\n\
The gyroscope activates, its gimbals increasing in speed as the crystal pendant illuminates.\n\
You feel a sharp pain in your chest, like a tug on your heart. The room dissolves around you into black.\n\
As the pain intensifies, a menacing laugh echoes in the dark. A voice thunders in your mind.\n\
\"One last failure to savor. How I will miss your arrogant attempts to traverse the forbidden.\"\n\
...\n\
Your body aches. The pain is unbearable.\n\
Rolling over, blades of grass tickle your skin.\n\
The taste of blood fills your mouth and breathing becomes difficult.\n\
You find yourself whispering, \"I'm sorry...\" as your breaths become shorter.\n\
Slowly, everything grows dark.\n\
\n\
You achieved the Bad Ending!\n\
Thank you for playing!\n"


# GOOD Ending occurs if you examine the gyroscope in the west room and you have the necklace and the logic board
goodEnding = "\nPlacing the pendant and logic board into the panel, you begin to feel vibrations deep below.\n\
The gyroscope activates, its gimbals increasing in speed as the crystal pendant illuminates.\n\
You feel a sharp pain in your chest, like a tug on your heart. The room dissolves around you into black.\n\
As the pain intensifies, a menacing roar can be heard from all around you.\n\
Then it stops.\n\
You are in a shabby garden. A young woman rises from her work, holding a flower that glows like the sun.\n\
She drops it upon seeing you. \"Trelle!\"\n\
You let out a sigh. \"Elana...\"\n\
\n\
You achieved the Good Ending!\n\
Thank you for playing!\n"

# User input parsing
# ------------------
# We use regular expressions to find matches for valid commands.
# These are called in our user_input function to determine what the appropriate response should be.

cmdMove = re.compile(("^(north|n|south|s|west|w|east|e|up|down){1}$"), re.I)
cmdExit = re.compile(("^(Quit|Exit){1}$"), re.I)
cmdInv = re.compile("^(Inventory){1}$", re.I)
cmdLook = re.compile(("^(Scan|Look){1}$"), re.I)
cmdHelp = re.compile(("^(Help){1}$"), re.I)
cmdExamine = re.compile(("^Examine\s((\w+)(?:\s)?){1,4}$"), re.I)
cmdTake = re.compile(("^Take\s((\w+)(?:\s)?){1,4}$"), re.I)

# Takes a String cmd and determines if it matches any regular expressions
# and responds accordingly.
def user_input(cmmd):
    if cmdExit.search(cmmd):                        # exits game if Player inputs "exit" or "quit"
        game_exit()
    elif cmdHelp.search(cmmd):                      # re-prints out the directions if the Player inputs "help"
        print_directions()
    elif cmdInv.search(cmmd):                       # prints out the contents of the Player's inventory
        p.print_inventory()
    elif cmdLook.search(cmmd):                      # prints out the description of the Player's Location
      print("\n\t~~" + p.location.name + "~~\n")
      print(p.location.description)                # when Player inputs "look"
    elif cmdExamine.search(cmmd):                   # prints out item's description if the Player types "examine"
        examine = cmdExamine.search(cmmd)
        examine = re.sub("examine ", "", examine.group(), 1)
        Player.examine_item(p, examine)
    elif cmdTake.search(cmmd):                      # Allows player to take an item if Player types "take"
        take = cmdTake.search(cmmd)
        take = re.sub("take ", "", take.group(), 1)
        p.take_item(take)
    elif cmdMove.search(cmmd):                      # Allows Player to move a given direction
        move = cmdMove.search(cmmd).group(0)
        Player.move(p, move)
    else:
        print("I don't know that command.")         # Prints if nothing matches our REs

# Player class
# Handles Player actions.
class Player:
    def __init__(self):
        self.location = main_room  # Player starts in the main room

    # take_item enables a Player to take an item from a Location as long as it exists in the world
    # and is takeable. Certain special items have special events.
    def take_item(self, item):
        if item not in itemTable:
            print("I don't recognize that item.")
        else:
            if itemTable[item][3]:  # If true, places item in player inventory
                self.location.remove_item(item)           # Removes the item from its location
                itemTable[item][1] = self                 # Changes the item's location value to the Player object
                print("\nYou take the " + item + '.\n')    # Prints out that the Player took the object
                # Handles special events if player takes specific items.
                if item == "logic board" and self.location == secret_room:
                    print("A loud, sharp pop rings through your skull. You find yourself back in the main room.\n")
                    self.location = main_room
                if item == "book" and self.location == south_room:
                    print("You sense that your bag is heavier than before.\n")
                    itemTable["tablet"][1] = self
            else:
                print("\nYou cannot take the " + item + ".\n")  # If item is not takeable, tell the Player


    # Moves Player object in a given direction, if valid.
    def move(self, direction):
        possibilities = ["north", "south", "east", "west"] # List of possible directions
        for possibility in possibilities:
            if direction == possibility[0] or direction == possibility: # Checks to see if there is a Location to
                if possibility in self.location.connections:            # move to in that direction
                    self.location.visited = True                        # Marks where the Player just was as visited
                    self.location = self.location.connections[possibility]  # Changes the Player's location to where they
                    self.location.print_description()                       # just moved and prints the description.
                else:
                    print("There's nowhere to go in that direction.")

    # Prints all items in Player's inventory
    def print_inventory(self):
        item_count = 0
        for item in itemTable:
            if itemTable[item][1] == self:
                item_count = item_count + 1
                print(item)
        if item_count == 0:
          print("There are no items in your inventory.")

    # Prints description of examined item
    def examine_item(self, item):
      if item == "socket" and itemTable["key"][1] == self:
        itemTable["key"][1] = None
        print("\nThe key scrapes stone but turns with a click.\
        \nA piece of the wall descends into the ground, revealing steps.\
        \nYou descend downward.\n")
        self.location = secret_room
        self.location.print_description()
      elif item == "gyroscope" and self.location == west_room:
        if itemTable["necklace"][1] == self and itemTable["tablet"][1] == self:
          print(badEnding)  # lose condition/bad ending
          raise SystemExit
        elif itemTable["necklace"][1] == self and itemTable["logic board"][1] == self:  # win condition
          print(goodEnding)
          raise SystemExit
        else:
          print(itemTable[item][0])
      elif item == "chair" and self.location == north_room:
        the_chair()
      elif item in itemTable and (itemTable[item][1] == self or itemTable[item][1] == self.location):
        print(itemTable[item][0])  # Only print out the description if the item exists in the world
                                  # and is located on the Player or in the Player's location
      else:
        print("There is no " + item + " to examine.")
        # Otherwise, notify the Player that there is no item to examine.

# A special chair that could make you go nutty
def the_chair():
    print("\nConcentrating on the chair, you notice a hum.\
    \nThe sound seems to be coming from the chair itself.\
    \nListening intently, the sound could almost be...a voice.\n")
    choice = input("Say something to the chair? (Y/N): ",)
    if choice.lower() == "y":   # lose condition
        print("\nObviously mad from your experience in this realm,\
        \nyou embrace insanity and address the chair.\
        \nThe conversation is better than you could have hoped for.\
        \nUnfortunately, it is much too good to pull yourself away for sustenance.\
        \nYou starve to death.")
        game_exit()
    else:
        print("\nYou shake off your momentary loss with reality and\n\
        find that the chair is in fact only a chair.\n")

# Prints introduction text once at start of game.
def print_intro(name):
    print("A w a k e n . . . " + name)
    print("Your body aches. There is flowing water, somewhere, but you cannot tell where.\n\
Rolling over, blades of grass tickle your skin and the smell of ash brings\n\
burning tears. As you wipe your eyes, the surrounding structure comes into focus.\n\
You look around and discover you are in the ... ")
    Location.print_description(main_room)

# Prints welcome message on game start.
def prompt_to_play():
    prompt = messagebox.askyesno("Welcome to Stargate: SCSI:1", "Start a new game?", parent=window)
    return prompt

# Print game directions initially after game start, and displays help menu during any time of the game.
def print_directions():

    messagebox.showinfo("Navigation", """To navigate the game world, type the following commands:\n\n\
    MOVEMENT\n\
    Move north: n/north\n\
    Move south: s/south\n\
    Move west: w/west\n\
    Move east: e/east\n\n\
    INTERACTIONS\n\
    Check inventory: inventory\n\
    Take item: take [item]\n\
    Look around: look/scan\n\
    Examine object: examine [object]\n\
    Exit game: quit/exit\n\n\
To access this help menu at any time, type \"help\".\n""", parent=window)

# popup window to request user name
def user_name():
    name = simpledialog.askstring("NAME", "Greetings, adventurer. What is your name?",
                                    parent=window)

    return name

# requests user name
def get_user_name():
    name = None
    while (name is None):
        name = user_name()
    return name

# prompts user for movement
def run_game():
    while True:
        #Prompt user for movement
        user_input(input(">>>", ))
        # Go to room and allow commands

# exits game
def game_exit():
    print("\nGame over. Thanks for playing!")
    raise SystemExit

# Drives the whole game.
def go():
    print_directions()
    name = get_user_name()
    print_intro(name)
    #Run until exit or player dies
    run_game()


p = Player()
game_init()







