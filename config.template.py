#!/usr/bin/env python3
# coding: utf-8

# I despite this people, but over all, I despite myself
import pickle
import os

# General
CommandPrefix = "!"  # Prefix for the Discord commands.
TOKEN         = r''  # Discord Bot Token; Note: if you try to use a user token you will get that account banned. 
PATH          = os.getcwd()  # Path where the system will deploy


# Admin staff
DevLab        = []    # Internal use... :shrug: (List of server id's as int)
SUPERUSER     = []  # List of superusers (id as int) that will have control over special system commands

## Logs
LogChan       = []    # List of channels where to tump logs (TODO: separate ERR_LogChan and Log_LogChan).
LogAdmin      = []    # List of users to ping when an error cours (will "try:" to log to LogChan).
LogToFile     = False # Bool, Create log file or not

# Exclude Lists
GildExList    = []  # List of guilds (id as int) excluded from markov recreation.
ChanExList    = []  # List of users (id as int) excluded from markov recretion.
UserExLixt    = []  # List of channels (id as int) excluded from markov recretion.

# Daily messag funtion
DayList       = [(False, ""), (False, ""), (True, PATH + r"/db/img/W.png"), (True, PATH + r"J.gif"), (True, PATH + r"V.jpg"), (False, ""), (False, "")] # I dont have willpower to explain this to you, go figure it by yourself lol (TODO: Properly document this function)
DayChan       = []    # Same comment as as DayList

### DEPRECATED; SEE -> LUXTER77/HIJACKED-ROLE
## Roll
#RolVChan      = []  # List of voice channels (id as int) where to execute the Roll_DB subsystem

# Miscelaneous
WeapList      = ['Emojis', 'Cringe', 'A chainsaw', 'Comnism', 'Capitalism', 'Anarchism', 'Memes', 'An informatic virus', "Yo' mama", 'The BFG', "It's own guts", 'My bare fists', 'Extraneous furry imagery', 'An orbital strike', 'A rocket launcher', 'A specially annoying kid with aspergers', 'An assault rifle', 'A Heaby machinegun', "It's own arms", 'A nuclear bomb', 'Puppies', 'javascript', 'Oracle®', 'EvilCorp', 'literally me', 'A giantic book', 'the power of God and anime'] #WeapList is a list for weapons to use on the punch command, probably will get deprecated in the future...
EmoteNest     = [[[""],[""]]] # list of iteractions(iteraction(trigger, discord.reaction(emoji).id))

# Why do I keep doing this to myself
pickle.dump(tuple((CommandPrefix, TOKEN, PATH, DevLab, LogChan, LogAdmin, WeapList, SUPERUSER, UserExLixt, ChanExList, GildExList, DayList, DayChan, EmoteNest)), open("Config.pkl", "wb"))