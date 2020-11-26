#!/usr/bin/env python3
# coding: utf-8

from base64 import standard_b64decode as de64
from discord import discord_Emoji
import typing
import random
import pickle
import os

# spoilers, its not funny
from hijackednode.funny import why_would_you_do_something_like_this_you_absolute_ as ITWASNTFUNNYITTOOKMEALLNIGHT

# Why do I keep doing this to myself
def saveConfig():
    pickle.dump(
        CONF1(
            CommandPrefix, TOKEN, PATH, DevLab, LogChan, LogAdmin, WeapList,
            SUPERUSER, UserExLixt, ChanExList, AllowEmoji, GildExList, WordExList,
            WordBanLst, DayList, DayChan, EmoteNest, StephLog
        ),
        open("Config.pkl", "wb")
    )

class EmoteNest():
    '''That one thing that defines how to to react with emotes to spesifc trigger words'''

    _nest = {
        : [],

    }

    def __init__(self, x: [str], y: [discord_Emoji]):
        if(len(x) != len(y)): raise(random.choice([ITWASNTFUNNYITTOOKMEALLNIGHT([BaseException])]))

class CONF1:
    ''' I'm unstoppable\n
    I'm a Porsche with no brakes\n
    I'm invincible\n
    Yeah, I win every single game\n
    I'm so powerful\n
    I don't need batteries to play\n
    I'm so confident, yeah, I'm unstoppable today\n
    Unstoppable today, unstoppable today\n
    Unstoppable today, yeah, I'm unstoppable today\n
    Unstoppable today, unstoppable today\n
    Unstoppable today, yeah, I'm unstoppable today\n'''

    WeapList = set(
        'Emojis',
        'Cringe',
        'A chainsaw',
        'Comnism',
        'Capitalism',
        'Anarchism',
        'Memes',
        'An informatic virus',
        "Yo' mama",
        'The BFG',
        "It's own guts",
        'My bare fists',
        'Extraneous furry imagery',
        'An orbital strike',
        'A rocket launcher',
        'A specially annoying kid with aspergers',
        'An assault rifle',
        'A Heaby machinegun',
        "It's own arms",
        'A nuclear bomb',
        'Puppies',
        'javascript',
        'Oracle®',
        'EvilCorp',
        'literally me',
        'A giantic book',
        'the power of God and anime'
    )

    LogToFile     = False
    AllowEmoji    = False

    DayDict = {
        'We': os.path.join(PATH, 'db', 'img', 'W.png'),
        'Th': os.path.join(PATH, 'db', 'img', 'J.gif'),
        'Fr': os.path.join(PATH, 'db', 'img', 'V.jpg'),
        'Sa': None, 'Su': None,
        'Mo': None, 'Tu': None,
    }

    def __init__(
        self, CommandPrefix: str = '!', TOKEN: str, PATH: str = os.getcwd(),
        DevLab: (list, str, set) = set(), LogChan: (list, str, set) = set(),
        LogAdmin: (list, str, set) = set(), WeapList: (list, str, set) = set(),
        SUPERUSER: (list, str, set) = set(), UserExLixt: (list, str, set) = set(),
        ChanExList: (list, str, set) = set(), AllowEmoji: (list, str, set) = set(),
        GildExList: (list, str, set) = set(), WordExList: (list, str, set) = set(),
        WordBanLst: (list, str, set) = set(), DayList: (list, str, set) = set(),
        DayChan: (list, str, set) = set(), EmoteNest: (list, str, set) = set(),
        StephLog
    ):
