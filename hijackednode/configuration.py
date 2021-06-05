from typing import Union, List, Set, NamedTuple
from collections import UserDict

import json
import os

from os.path import join

from base64 import standard_b64decode as de64

from discord import User, TextChannel, Guild

from .funny import Pain  # spoilers, its not funny

if(os.name == "nt"):
    import ctypes.wintypes
else:
    import subprocess

def _get_def_doc() -> str:
    "Get Documents folder"
    if(os.name == "nt"):
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        return(str(buf.value))
    else:
        try:
            return(subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines=True).strip())
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(str(e), "\n\tI'm gonna try to guess the user and use the place I feel like using...\n")
            return join('/home', os.environ['USER'], 'Docuements')

_WeapList = set([
    "Emojis", "Cringe", "A chainsaw", "Communism", "Capitalism", "Anarchism",
    "Memes", "An Informatic virus", "Yo' mama", "The BFG", "It's own guts",
    "My bare fists", "A gigantic book", "Extraneous furry imagery",
    "An orbital strike", "Oracle®", "A rocket launcher", "Margaret Teacher",
    "A specially annoying kid with aspergers", "An assault rifle",
    "A Heavy machinegun", "It's own arms", "A nuclear bomb", "Puppies",
    "javascript", "EvilCorp", "literally me", "the power of God and anime",
])

_PATH = join(_get_def_doc(), "Hijacked-Node")

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
    We: DayCheckType  # join(PATH, "db", "img", "We.png"),
    Th: DayCheckType  # join(PATH, "db", "img", "Jh.gif"),
    Fr: DayCheckType  # join(PATH, "db", "img", "Fr.jpg"),
    Sa: DayCheckType  # join(PATH, "db", "img", "Sa.jpg"),
    Su: DayCheckType  # join(PATH, "db", "img", "Su.jpg"),
    Mo: DayCheckType  # join(PATH, "db", "img", "Mo.jpg"),
    Tu: DayCheckType  # join(PATH, "db", "img", "Tu.jpg"),

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
                 TOKEN: str = False,
                 DevLab: DiscordGuildType = set(),
                 LogChan: DiscordChannelType = set(),
                 LogAdmin: DiscrodUserType = set(),
                 SUPERUSER: DiscrodUserType = set(),
                 UserExLixt: DiscrodUserType = set(),
                 ChanExList: DiscordChannelType = set(),
                 GildExList: DiscordGuildType = set(),
                 WordExList: WordsType = set(),
                 WordBanLst: WordsType = set(),
                 SpecDate: List[dict] = [],
                 DailyDict: DailyDictType = set(),
                 DailyChan: DiscordChannelType = set(),
                 EmoteNest: EmoteNestType = set(),
                 CommandPrefix: str = "!",
                 PATH: str = _PATH,
                 LogToFile: bool = False,
                 AllowEmoji: bool = False,
                 WeapList: WeapListType = _WeapList,
                 DoLoadFile: bool = True,
                 PrefBanLst: Set[str] = set(),
                 StephLogs: bool = False,
                 ):
        self.TOKEN = TOKEN
        self.DevLab = DevLab
        self.LogChan = LogChan
        self.LogAdmin = LogAdmin
        self.SUPERUSER = SUPERUSER
        self.UserExLixt = UserExLixt
        self.ChanExList = ChanExList
        self.GildExList = GildExList
        self.WordExList = WordExList
        self.WordBanLst = WordBanLst
        self.SpecDate = SpecDate
        self.DailyDict = DailyDict
        self.DailyChan = DailyChan
        self.EmoteNest = EmoteNest
        self.CommandPrefix = CommandPrefix
        self.DoLoadFile = DoLoadFile
        self.PATH = PATH
        self.LogToFile = LogToFile
        self.AllowEmoji = AllowEmoji
        self.WeapList = WeapList
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
                os.makedirs(join(self.PATH, x), exist_ok=True)
            else:
                self.ch_dirs(tree[x])

    def save(self):
        try:
            with open(join(self.PATH, "config.json")) as confile:
                json.dump(confile, confile, indent=4, sort_keys=True)
        except Exception:
            Pain(BaseException)  # Hug you Loop

    def load(self):
        try:
            data = json.load(open(join(self.PATH, "config.json"), "rb"))
            self.TOKEN = data.get('TOKEN')
            self.DevLab = data.get('DevLab')
            self.LogChan = data.get('LogChan')
            self.LogAdmin = data.get('LogAdmin')
            self.SUPERUSER = data.get('SUPERUSER')
            self.UserExLixt = data.get('UserExLixt')
            self.ChanExList = data.get('ChanExList')
            self.GildExList = data.get('GildExList')
            self.WordExList = data.get('WordExList')
            self.WordBanLst = data.get('WordBanLst')
            self.SpecDate = data.get('SpecDate')
            self.DailyDict = data.get('DailyDict')
            self.DailyChan = data.get('DailyChan')
            self.EmoteNest = data.get('EmoteNest')
            self.CommandPrefix = data.get('CommandPrefix')
            self.DoLoadFile = data.get('DoLoadFile')
            self.PATH = data.get('PATH')
            self.LogToFile = data.get('LogToFile')
            self.AllowEmoji = data.get('AllowEmoji')
            self.WeapList = data.get('WeapList')
            self.PrefBanLst = data.get('PrefBanLst')
            self.StephLogs = data.get('StephLogs')
        except FileNotFoundError:
            pass  # ex dee
        except Exception:
            Pain(BaseException)  # Hug you Loop
            pass  # ex dee
