from typing import Union, List, Set, NamedTuple
from collections import UserDict

import random
import pickle
import os

from base64 import standard_b64decode as de64
from discord import User, TextChannel, Guild, Emoji

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
        return(subprocess.check_output(
            ["xdg-user-dir", "DOCUMENTS"], universal_newlines=True
        ).strip())

_WeapList = set([
    "Emojis", "Cringe", "A chainsaw", "Comnism", "Capitalism", "Anarchism",
    "Memes", "An informatic virus", "Yo' mama", "The BFG", "It's own guts",
    "My bare fists", "A giantic book", "Extraneous furry imagery",
    "An orbital strike", "Oracle®", "A rocket launcher",
    "A specially annoying kid with aspergers", "An assault rifle",
    "A Heaby machinegun", "It's own arms", "A nuclear bomb", "Puppies",
    "javascript", "EvilCorp", "literally me", "the power of God and anime"
])

_PATH = os.path.join(_get_def_doc(), "Hijacked-Node")


EmoteNestType = List[List[Union[str, Emoji]]]
DiscordChannelType = Set[Union[str, int, TextChannel]]
DiscordGuildType = Set[Union[str, int, Guild]]
DiscrodUserType = Set[Union[str, int, User]]
WeapListType = Union[Set[str], List[str]]
WordsType = Set[str]
class dayType(NamedTuple):
    enabled: bool = False
    fle: str = None
    msg: str = ''

class DailyType(NamedTuple):
    Mo: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Mo.jpg"), msg=''),
    Tu: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Tu.jpg"), msg=''),
    We: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "We.jpg"), msg=''),
    Th: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Th.jpg"), msg=''),
    Fr: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Fr.jpg"), msg=''),
    Sa: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Sa.jpg"), msg=''),
    Su: dayType = dayType(enabled=False, fle=os.path.join(_PATH, "db", "img", "Su.jpg"), msg=''),
    days: list = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

class CONF0():
    'Unified Configuration Object'
    # Please update here too if you modify parameters
    __params__ = [
        'TOKEN', 'DevLab', 'LogChan', 'LogAdmin', 'SUPERUSER', 'UserExLixt',
        'ChanExList', 'GildExList', 'WordExList', 'WordBanLst', 'DailyDict',
        'DailyChan', 'EmoteNest', 'CommandPrefix', 'PATH', 'LogToFile',
        'AllowEmoji', 'WeapList'  # , 'StephLog',
    ]
    __TreeDir__ = ['img', 'txt', 'wsp']

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
                 DailyDict: DailyType = DailyType(),
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
        for x in self.__TreeDir__:
            os.makedirs(os.path.join(self.PATH, x), exist_ok=True)
        if(DoLoadFile):
            self.load_from_file()

    def save_save_to_file(self):
        try:
            pickle.dump(self, open(os.path.join(self.PATH, "Config.pkl"), "wb"))
        except Exception:
            Pain(BaseException)  # Hug you Loop

    def load_from_file(self):
        'Like that one Matrix moive'
        try:
            new_self = pickle.load(open(os.path.join(self.PATH, "Config.pkl"), "rb"))
            self.TOKEN = new_self.TOKEN
            self.DevLab = new_self.DevLab
            self.LogChan = new_self.LogChan
            self.LogAdmin = new_self.LogAdmin
            self.SUPERUSER = new_self.SUPERUSER
            self.UserExLixt = new_self.UserExLixt
            self.ChanExList = new_self.ChanExList
            self.GildExList = new_self.GildExList
            self.WordExList = new_self.WordExList
            self.WordBanLst = new_self.WordBanLst
            self.DailyDict = new_self.DailyDict
            self.DailyChan = new_self.DailyChan
            self.EmoteNest = new_self.EmoteNest
            self.CommandPrefix = new_self.CommandPrefix
            self.PATH = new_self.PATH
            self.LogToFile = new_self.LogToFile
            self.AllowEmoji = new_self.AllowEmoji
            self.WeapList = new_self.WeapList
            # self.StephLog = StephLog
        except Exception:
            Pain(BaseException)  # Hug you Looooooop

days = DailyType(
    dayType(check=False, fle='Mo', dint=0),
    dayType(check=False, fle='Tu', dint=1),
    dayType(check=False, fle='We', dint=2),
    dayType(check=False, fle='Th', dint=3),
    dayType(check=False, fle='Fr', dint=4),
    dayType(check=False, fle='Sa', dint=5),
    dayType(check=False, fle='Su', dint=6),
)
