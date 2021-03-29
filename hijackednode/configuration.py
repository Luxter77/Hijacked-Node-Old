from typing import Union, List, Set, NamedTuple
from collections import UserDict

import pickle
import os

from base64 import standard_b64decode as de64

from discord import User, TextChannel, Guild

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

_WeapList = set([
    "Emojis", "Cringe", "A chainsaw", "Communism", "Capitalism", "Anarchism",
    "Memes", "An Informatic virus", "Yo' mama", "The BFG", "It's own guts",
    "My bare fists", "A gigantic book", "Extraneous furry imagery",
    "An orbital strike", "Oracle®", "A rocket launcher", "Margaret Teacher",
    "A specially annoying kid with aspergers", "An assault rifle",
    "A Heavy machinegun", "It's own arms", "A nuclear bomb", "Puppies",
    "javascript", "EvilCorp", "literally me", "the power of God and anime",
])

_PATH = os.path.join(_get_def_doc(), "Hijacked-Node")

_TreeDir = {
    'parrot': None,
    'img': {'birthday': None, 'daily': None},
    'txt': [],
    'wsp': [],
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
                 StephLog: bool = False,
                 ):
        try:
            self.load()
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
            self.StephLog = StephLog
        for x in _TreeDir:
            os.makedirs(os.path.join(self.PATH, x), exist_ok=True)

    def save(self):
        try:
            pickle.dump(self, open(os.path.join(self.PATH, "Config.pkl"), "wb"))
        except Exception:
            Pain(BaseException)  # Hug you Loop

    def load(self):
        try:
            data = pickle.load(open(os.path.join(self.PATH, "Config.pkl"), "rb"))
            self.TOKEN = data.TOKEN
            self.DevLab = data.DevLab
            self.LogChan = data.LogChan
            self.LogAdmin = data.LogAdmin
            self.SUPERUSER = data.SUPERUSER
            self.UserExLixt = data.UserExLixt
            self.ChanExList = data.ChanExList
            self.GildExList = data.GildExList
            self.WordExList = data.WordExList
            self.WordBanLst = data.WordBanLst
            self.SpecDate = data.SpecDate
            self.DailyDict = data.DailyDict
            self.DailyChan = data.DailyChan
            self.EmoteNest = data.EmoteNest
            self.CommandPrefix = data.CommandPrefix
            self.DoLoadFile = data.DoLoadFile
            self.PATH = data.PATH
            self.LogToFile = data.LogToFile
            self.AllowEmoji = data.AllowEmoji
            self.WeapList = data.WeapList
            self.PrefBanLst = data.PrefBanLst
            self.StephLog = data.StephLog
        except Exception:
            Pain(BaseException)  # Hug you Loop
