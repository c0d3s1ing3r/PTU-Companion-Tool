# this file handles player character creator logic and whatnot, and can be ran as a driver, text-based class, but is meant to be imported to the GUI class
# in addition, it also intended to handle the logic for easy custom character creation

import json
import random
import playsound
import threading

class Trainer:
    def __init__(self):
        self.name = ""
        self.gender = ""
        self.age = -1
        self.background = ""
        self.height = ""
        self.weight = ""
        self.description = ""
        self.pokemon = list()

def randomSong():
    which_song = random.randint(1,3)
    if which_song == 1:
        playsound.playsound("Welcome to the World of Pokemon - Pokemon DiamondPearlPlatinum OST.mp3")
    elif which_song == 2:
        playsound.playsound("Welcome to the World of Pokemon - Pokemon Origins.mp3")
    else:
        playsound.playsound("Welcome to the World of Pokemon Piano Cover - Pokemon Diamond And Pearl.mp3")

# driver code
def playerCreation():
    audiothread = threading.Thread(target=randomSong)
    audiothread.start()
    player = Trainer()
    print("Hello, and welcome to the wonderful world of Pokemon!\nMy Name is Professor Cypress, and I'm the Pokemon Professor for this region")
    userin = input("It's an absolute pleasure to meet you, but I can't quite see you yet. For starters, are you a boy; or a girl?\n")
    man = ("MALE", "MAN", "M", "B", "BOY", "GUY", "DICK", "DUDE")
    woman = ("FEMALE", "WOMAN", "W", "G", "GIRL", "GAL", "BITCH", "DUDETTE")
    while userin.upper() not in man and userin.upper() not in woman:
        userin = input("Err, sorry, I didn't catch that. Could you please repeat that?\n")
    if userin.upper() in man:
        player.gender = "Male"
    elif userin.upper() in woman:
        player.gender = "Female"
    else:
        player.gender = "ERROR"

    if player.gender == "Male":
        userin = input("It's great to meet you sir! Well then, what's your name?\n")
    elif player.gender == "Female":
        userin = input("It's great to meet you ma'am! Well then, what's your name?\n")
    player.name = userin

    userin = input("Ok then " + player.name + "! How old are you?\n")
    while not userin.isdigit() or int(userin) < 0 or int(userin) > 99:
        userin = input("Ohoho very funny " + player.name + ", but let's be serious now.\n")
    player.age = int(userin)

    userin = input("Well then " + player.name + ", why don't you tell me a bit about yourself?\n")
    player.backstory = userin

    userin = input("Well then, now it's time to determine some of your vital statistics.\nDo you already know those? or do you need some help figuring those out?\n")
    
    
    #stats = (player.intelligence, player.strength, player.wisdom, player.charisma, player.dexterity, player.constitution)
    #NOTE TO SELF: use the stats along with the palyers stats to recommend a basic profession
    #NOTE TO SELF: KILL MUSIC THREAD WHEN FINISHED

def npcCreation():
    pass

if __name__ == "__main__":
    userin = input("Hello and welcome to the PokeD&D Character creator. Would you like to create a new player character (PC); or just spin up a random NPC?\n")
    pc_responses = ("PC", "NEW CHARACTER", "NEW PLAYER", "PLAYER CHARACTER")
    npc_responses = ("NPC", "NON-PLAYER CHARACTER", "NONPLAYER CHARACTER", "NON PLAYER CHARACTER")
    while userin.upper() not in pc_responses and userin.upper() not in npc_responses:
        userin = input("I didn't quite get that, please try again.\n")
    
    if userin.upper() in pc_responses:
        playerCreation()
    elif userin.upper() in npc_responses:
        npcCreation()
    else:
        print("NO ACCEPTABLE INPUT / REALLY STRANGE ERROR")
