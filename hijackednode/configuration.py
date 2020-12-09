from typing import Union, List, Set
from collections import NamedTuple, UserDict

import random
import pickle
import os

from base64 import standard_b64decode as de64
from discord import User, TextChannel, Guild, discord_Emoji

from hijackednode.funny import Pain  # spoilers, its not funny

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
        return(subprocess.check_output(
            ["xdg-user-dir", "DOCUMENTS"], universal_newlines=True
        ).strip())

_WeapList = set(
    "Emojis", "Cringe", "A chainsaw", "Comnism", "Capitalism", "Anarchism",
    "Memes", "An informatic virus", "Yo' mama", "The BFG", "It's own guts",
    "My bare fists", "A giantic book", "Extraneous furry imagery",
    "An orbital strike", "Oracle®", "A rocket launcher",
    "A specially annoying kid with aspergers", "An assault rifle",
    "A Heaby machinegun", "It's own arms", "A nuclear bomb", "Puppies",
    "javascript", "EvilCorp", "literally me", "the power of God and anime"
)

_PATH = os.path.join(_get_def_doc(), "Hijacked-Node")

_TreeDir = [
    'img',
    'txt',
    'wsp',
]

EmoteNestType = List[List[str, Union[str, discord_Emoji]]]
DiscordChannelType = Set[Union[str, int, TextChannel]]
DiscordGuildType = Set[Union[str, int, Guild]]
DiscrodUserType = Set[Union[str, int, User]]
WeapListType = Union[Set[str], List[str]]
WordsType = Set[str]
class dayCheckType(NamedTuple):
    check: bool
    fle: str
    dint: int

class DailyDictType(UserDict):
    We: dayCheckType  # os.path.join(PATH, "db", "img", "We.png"),
    Th: dayCheckType  # os.path.join(PATH, "db", "img", "Jh.gif"),
    Fr: dayCheckType  # os.path.join(PATH, "db", "img", "Fr.jpg"),
    Sa: dayCheckType  # os.path.join(PATH, "db", "img", "Sa.jpg"),
    Su: dayCheckType  # os.path.join(PATH, "db", "img", "Su.jpg"),
    Mo: dayCheckType  # os.path.join(PATH, "db", "img", "Mo.jpg"),
    Tu: dayCheckType  # os.path.join(PATH, "db", "img", "Tu.jpg"),

class CONF0():
    'Unified Configuration Object'
    # Please update here too if you modify parameters
    __params__ = [
        'TOKEN', 'DevLab', 'LogChan', 'LogAdmin', 'SUPERUSER', 'UserExLixt',
        'ChanExList', 'GildExList', 'WordExList', 'WordBanLst', 'DailyDict',
        'DailyChan', 'EmoteNest', 'CommandPrefix', 'PATH', 'LogToFile',
        'AllowEmoji', 'WeapList'  # , 'StephLog',
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
                 DailyDict: DailyDictType = set(),
                 DailyChan: DiscordChannelType = set(),
                 EmoteNest: EmoteNestType = set(),
                 CommandPrefix: str = "!",
                 PATH: str = _PATH,
                 LogToFile: bool = False,
                 AllowEmoji: bool = False,
                 WeapList: WeapListType = _WeapList,
                 DoLoadFile: bool = True,
                 # StephLog: type
                 ):
        try:
            self.load(path=self.PATH)
        except Exception:
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
            self.DailyDict = DailyDict
            self.DailyChan = DailyChan
            self.EmoteNest = EmoteNest
            self.CommandPrefix = CommandPrefix
            self.PATH = PATH
            self.LogToFile = LogToFile
            self.AllowEmoji = AllowEmoji
            self.WeapList = WeapList
            # self.StephLog = StephLog
        for x in _TreeDir:
            os.makedirs(os.path.join(self.PATH, x), exist_ok=True)

    def save(self):
        try:
            pickle.dump(self, open(os.path.join(self.PATH, "Config.pkl"), "wb"))
        except Exception:
            Pain(BaseException)  # Hug you Loop

    def load(self):
        try:
            self = pickle.load(open(os.path.join(self.PATH, "Config.pkl"), "rb"))
        except Exception:
            Pain(BaseException)  # Hug you Loop