#!/usr/bin/env python3
'''TheEyeLoop said to me if I where to do something like this it would be funny.\n
I, of course, did instantly hiperfixated and did it.
This was a mistake.'''

# :(
from random import choice

from typing import Union, List, Set, NamedTuple
from collections import UserDict

from base64 import standard_b64decode as de64

from discord import User, TextChannel, Guild

import os

if(os.name == "nt"):
    import ctypes.wintypes
else:
    import subprocess

from json.decoder import JSONDecodeError
from random import choice, randint

from emoji import EMOJI_UNICODE_ENGLISH
from copy import deepcopy
from typing import List
from flask import Flask

import subprocess as sp
import unicodedata
import asyncio
import json
import re

class Pain():
    '''
    # You may be asking now:\n
    #    Luxter, why the hug did you make this into a class instead of a recursive function\n
    # I answer:\n
    #    You expect too much out of this dumpster fire of a module.\n
    UPDATE: hug you Loop\n
    UPDATE: THIS IS HARDER THAN IT LOOKS\n
    UPDATE: IT TOOK ME ALL NIGHT BUT I DID IT! self.laugh_maniatically()
    '''

    def why_would_you_do_something_like_this_you_absolute_(self, downstream: list) -> set:
        outstream = []
        for x in downstream:
            if(x.__subclasses__()):
                outstream += list(
                    self.why_would_you_do_something_like_this_you_absolute_(downstream=x.__subclasses__())
                )
            outstream.append(x)
        return(set(outstream))
        # IN THE END IT WAS SO SIMPLE WHY THE HUG DID I OVERCOMPLICATE MYSELF ALL THE WAY ONTO HELL

    def __init__(self, pain):
        print("Hug you Loop.")
        raise(choice(list(self.why_would_you_do_something_like_this_you_absolute_([pain]))))

def _get_def_doc() -> str:
    "Get Documents folder"
    if(os.name == "nt"):
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        return(str(buf.value))
    else:
        return(subprocess.check_output(
            ["xdg-user-dir", "DOCUMENTS"], universal_newlines=True
        ).strip())

_PATH = os.path.join(_get_def_doc(), "Hijacked-Node")

_WeapList = set([
    "Emojis", "Cringe", "A chainsaw", "Communism", "Capitalism", "Anarchism",
    "Memes", "An Informatic virus", "Yo' mama", "The BFG", "It's own guts",
    "My bare fists", "A gigantic book", "Extraneous furry imagery",
    "An orbital strike", "Oracle®", "A rocket launcher", "Margaret Teacher",
    "A specially annoying kid with aspergers", "An assault rifle",
    "A Heavy machinegun", "It's own arms", "A nuclear bomb", "Puppies",
    "javascript", "EvilCorp", "literally me", "the power of God and anime",
])


_TreeDir = {
    'parrot': None,
    'img': {
        'birthday': None,
        'daily': None
    },
    'txt': None,
    'wsp': None,
}

EmoteNestType = List[List[str]]
DiscordChannelType = Set[Union[str, int, TextChannel]]
DiscordGuildType = Set[Union[str, int, Guild]]
DiscrodUserType = Set[Union[str, int, User]]
WeapListType = Union[Set[str], List[str]]
WordsType = Set[str]

class DayCheckType(NamedTuple):
    check: bool
    fle: str
    dint: int

class DailyDictType(UserDict):
    We: DayCheckType  # os.path.join(PATH, "db", "img", "We.png"),
    Th: DayCheckType  # os.path.join(PATH, "db", "img", "Jh.gif"),
    Fr: DayCheckType  # os.path.join(PATH, "db", "img", "Fr.jpg"),
    Sa: DayCheckType  # os.path.join(PATH, "db", "img", "Sa.jpg"),
    Su: DayCheckType  # os.path.join(PATH, "db", "img", "Su.jpg"),
    Mo: DayCheckType  # os.path.join(PATH, "db", "img", "Mo.jpg"),
    Tu: DayCheckType  # os.path.join(PATH, "db", "img", "Tu.jpg"),

class CONF0():
    'Unified Configuration Object'
    # Please update here too if you modify parameters
    __params__ = [
        'TOKEN', 'DevLab', 'LogChan', 'LogAdmin', 'SUPERUSER', 'UserExLixt',
        'ChanExList', 'GildExList', 'WordExList', 'WordBanLst', 'DailyDict',
        'DailyChan', 'EmoteNest', 'CommandPrefix', 'PATH', 'LogToFile',
        'AllowEmoji', 'WeapList', 'StephLogs',
    ]

    def __init__(self,
                 WordExList: WordsType = set(),
                 WordBanLst: WordsType = set(),
                 SpecDate: List[dict] = [],
                 PATH: str = _PATH,
                 DoLoadFile: bool = True,
                 PrefBanLst: Set[str] = set(),
                 StephLogs: bool = [],
                 ):
        self.WordExList = WordExList
        self.WordBanLst = WordBanLst
        self.SpecDate = SpecDate
        self.DoLoadFile = DoLoadFile
        self.PATH = _PATH
        self.PrefBanLst = PrefBanLst
        self.StephLogs = StephLogs
        try:
            self.load()
        except Exception:
            pass  # oh well, I did my best :shrug:
        self.ch_dirs(_TreeDir)

    def ch_dirs(self, tree: dict):
        for x in tree:
            if tree[x] is None:
                os.makedirs(os.path.join(self.PATH, x), exist_ok=True)
            else:
                self.ch_dirs(tree[x])

    def save(self):
        try:
            with open(os.path.join(self.PATH, "config.json")) as confile:
                json.dump(confile, confile, indent=4, sort_keys=True)
        except Exception:
            Pain(BaseException)  # Hug you Loop

    def load(self):
        try:
            data = json.load(open(os.path.join(self.PATH, "config.json"), "rb"))
            self.WordExList = data.get('WordExList')
            self.WordBanLst = data.get('WordBanLst')
            self.SpecDate = data.get('SpecDate')
            self.DoLoadFile = data.get('DoLoadFile')
            self.PATH = data.get('PATH')
            self.PrefBanLst = data.get('PrefBanLst')
            self.StephLogs = data.get('StephLogs')
        except FileNotFoundError:
            pass  # ex dee
        except Exception:
            Pain(BaseException)  # Hug you Loop
            pass  # ex dee

class TalkBoxError(Exception):
    ...  # Placeholder lol

# define FPCAMHHPC = "fuck pythonic code, all my homies hate pythonic code - this post was made by the perl gang"

def trans(text: str, ptq: str) -> str:
    if os.name != "nt":  # windows bad linux good
        # FPCAMHHPC
        process: sp.Popen = sp.Popen(["/usr/bin/apertium", ptq, "-u"], stdout=sp.PIPE, stdin=sp.PIPE)
        process.stdin.write(text.encode())
        text = process.communicate()[0].decode("utf-8")
    return text

def trans_back(text: str, org: str = 'es'):
    if org == 'en':
        return trans(trans(text, ptq='en-es'), ptq='es-en')
    elif org == 'es':
        return trans(trans(text, ptq='es-en'), ptq='en-es')
    else:
        raise(Exception('LangNotSupportedError'))

class TextPipeLine:
    'The thing that chews all the text and stuff'

    TEXT_PATCHES = {
        "forward": [("(", "",), (")", "",), ("[", "",), ("]", "",), ("{", "",), ("}", "",), ("*", "",), ('"', ''), ("-", " ",), ("\n", ". ",), ("_", "",), (":", " : ",), (";", " ; ",), (",", " , ",), (".", " . ",), ('  ', ' ',), ('  ', ' ',), (". . .", "...",), ('1', '⣿',), ('2', '⣿',), ('3', '⣿',), ('4', '⣿',), ('5', '⣿',), ('6', '⣿',), ('7', '⣿',), ('8', '⣿',), ('9', '⣿',), ('jsjs', 'jajaja',), ('jaja', 'jajaja',)],
        "backward": [(" :", ":",), (" ;", ";",), (" , ", ", ",), (" .", ".",), (" i ", " Yo ",)],
    }

    def __init__(self, config: CONF0):
        self.config: CONF0 = config

    def plex(self, text: str, direction: str = 'forward') -> str:
        # poor choice, but I don't care
        for x, y in (self.TEXT_PATCHES[direction]):
            text = text.replace(x, y)

        for patch in self.config.WordExList:
            text = text.replace(' ' + patch, '')
            text = text.replace(patch + ' ', '')
            text = text.replace(patch, '')

        if direction == 'backward':
            return re.sub("⣿", (lambda _: str(randint(0, 9))), text)
        else:
            return text

    def checks(self, skala: str) -> bool:
        if ((len(skala) < 6) or (len(skala.replace(" ", "")) / len(skala.split(" ")) <= 2) or not(set(skala).isdisjoint(set(EMOJI_UNICODE_ENGLISH.values()))) or not(set(skala).isdisjoint(set(self.config.WordBanLst)))):
            return False
        else:
            for banned in self.config.PrefBanLst:
                if skala.startswith(banned):
                    return False
        return True

    async def load_from_discord_dump(self) -> List[str]:
        "It's a bad multilingual pun"
        # WARNING: you should set up a lock outside from this function
        try:
            with open(os.path.join(self.config.PATH, "DB", "parrot.json"), 'r') as corp_file:
                chat_log   = json.load(corp_file)
                proto_corp = list()
        except JSONDecodeError:
            try:
                with open(os.path.join(self.config.PATH, "DB", "parrot.bkp.json"), 'r') as corp_file:
                    chat_log   = json.load(corp_file)
                    proto_corp = list()
            except FileNotFoundError:
                chat_log   = {'last_time': None}
            proto_corp = list()
        except FileNotFoundError:
            chat_log   = {'last_time': None}
            proto_corp = list()

        del chat_log['last_time']

        for server in chat_log:
            for channel in server:
                for message in channel:
                    message = str(message)
                    if self.checks(message):
                        proto_corp += await self.parse_message(message)
        return(proto_corp)

    async def load_from_steph_logs(self) -> List[str]:
        proto_corp = list()
        for steph_path in self.config.StephLogs:
            with open(steph_path, "r", encoding="utf-8") as steph_file:
                for line in steph_file.readlines():
                    line = line.lower()
                    if self.checks(line):
                        proto_corp += await self.parse_message(line)
        return(proto_corp)

    async def parse_message(self, text: str) -> List[str]:
        text = text.lower()

        for word in text.split(' '):
            if(len(word) > 14):
                text.replace(word, '')

        text = self.plex(unicodedata.normalize("NFC", text)).lower().split()  # FPCAMHHPC

        if (text[-1] == '.'):
            if (text[-2] == '.'):
                if (text[-3] == '.'):
                    text = text[:-2]
                else:
                    text = text[:-1]
        else:
            text = text + ['.']

        if bool(text):
            return text
        else:
            return []

class TalkBox:
    'This is where the magic happens'

    PULL_LOCK   = asyncio.Lock()  # Lock for pulling messages from discord servers
    TRANS_LOCK  = asyncio.Lock()  # Lock for trans_map AND all_text AND all_words AND chain
    CORPUS_LOCK = asyncio.Lock()  # Lock for the files on disk that hold the corpus

    def __init__(self):
        self.config: CONF0 = CONF0()
        self.pipeline = TextPipeLine(self.config)
        os.makedirs(os.path.join(self.config.PATH, "DB"), exist_ok=True)
        asyncio.run(self.load())

    async def load(self):
        async with self.TRANS_LOCK:
            async with self.CORPUS_LOCK:
                all_text: list = (await self.pipeline.load_from_steph_logs()) + (await self.pipeline.load_from_discord_dump())
            all_words: list = list(set(all_text))
            trans_map: dict = {'ntw': all_words, 'wtn': dict((x, i,) for i, x in enumerate(all_words))}
        chain = dict()

        t_primer = trans_map['wtn'][trans_map['ntw'][0]]
        for word in all_text:  # pylint: disable=not-an-iterable # are you bucking kidding me pylint? thats a list! how can it be non iterable???
            word = trans_map['wtn'][word]
            try:
                chain[t_primer].append(word)
            except KeyError:
                chain[t_primer] = [word]
            finally:
                t_primer = word

        self.chain = chain
        self.all_text = all_text
        self.all_words = all_words
        self.trans_map = trans_map

    def talk(self, end_word: str = '.', until: int = 5, max_length: int = 10, primer: str = False, init: List[str] = False) -> str:
        chain     = self.chain
        all_text  = self.all_text
        all_words = self.all_words
        trans_map = self.trans_map

        if bool(randint(0, 1)):
            until += randint(0, 2)
        else:
            until = max(until - randint(0, 6), until)

        if bool(primer) and not(init):
            sms = [trans_map['wtn'][primer]]
        elif bool(init):
            try:
                sms = [trans_map['wtn'][init[-1]]]
            except KeyError:
                sms = [trans_map['wtn'][choice(trans_map['ntw'])]]
        else:
            sms = [trans_map['wtn'][choice(trans_map['ntw'])]]

        while ((len(sms) < until) or (sms[-1] != trans_map['wtn'][end_word]) or not(len(sms) > max_length)):
            sms.append(choice(chain[sms[-1]]))

        sms = self.pipeline.plex(' '.join([trans_map['ntw'][word] for word in sms]), 'backward')

        sms = trans_back(sms)

        if bool(init):
            sms = ' '.join(init[:-1]) + " " + sms

        return(' '.join(x for x in sms.split(' ') if bool(x)).lower().capitalize())

talkbox = TalkBox()
app = Flask(__name__)

@app.route("/talk")
def talk():
    return(talkbox.talk())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
