from typing import Union, List, Set, Dict, NamedTuple
from collections import UserDict

import subprocess
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

DailyDict = {
    'Mo': {'enabled': False, 'fle': os.path.join(_PATH, "img", "Mo.jpg"), 'msg': ''},
    'Tu': {'enabled': False, 'fle': os.path.join(_PATH, "img", "Tu.jpg"), 'msg': ''},
    'We': {'enabled': True,  'fle': os.path.join(_PATH, "img", "We.png"), 'msg': ''},
    'Th': {'enabled': True,  'fle': os.path.join(_PATH, "img", "Th.gif"), 'msg': ''},
    'Fr': {'enabled': True,  'fle': os.path.join(_PATH, "img", "Fr.jpg"), 'msg': ''},
    'Sa': {'enabled': False, 'fle': os.path.join(_PATH, "img", "Sa.jpg"), 'msg': ''},
    'Su': {'enabled': False, 'fle': os.path.join(_PATH, "img", "Su.jpg"), 'msg': ''}
}


class CONF0():
    'Unified Configuration Object'
    # Please update here too if you modify parameters
    __params__ = [
        'TOKEN', 'DevLab', 'LogChan', 'LogAdmin', 'SUPERUSER', 'UserExLixt',
        'ChanExList', 'GildExList', 'WordExList', 'WordBanLst', 'PrefBanLst',
        'DailyDict', 'DailyChan', 'EmoteNest', 'CommandPrefix', 'PATH',
        'LogToFile', 'AllowEmoji', 'WeapList', 'StephLog',
    ]
    __TreeDir__ = ['img', 'txt', 'wsp', 'parrot']

    def __init__(self,
                 TOKEN: str = False,
                 DevLab: Set[Union[int, Guild]] = set(),
                 LogChan: Set[Union[int, TextChannel]] = set(),
                 LogAdmin: Set[Union[int, User]] = set(),
                 SUPERUSER: Set[Union[int, User]] = set(),
                 UserExLixt: Set[Union[int, User]] = set(),
                 ChanExList: Set[Union[int, TextChannel]] = set(),
                 GildExList: Set[Union[int, Guild]] = set(),
                 WordExList: Set[str] = set(),
                 WordBanLst: Set[str] = set(),
                 PrefBanLst: Set[str] = set(),
                 DailyDict: Dict[str, Dict[str, Union[bool, str]]] = DailyDict,
                 DailyChan: Set[Union[int, TextChannel]] = set(),
                 EmoteNest: List[List[Union[str, Emoji]]] = list(),
                 CommandPrefix: str = "!",
                 PATH: str = _PATH,
                 LogToFile: bool = False,
                 AllowEmoji: bool = False,
                 WeapList: Union[Set[str], List[str]] = _WeapList,
                 DoLoadFile: bool = True,
                 StephLog: bool = False,
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
        self.PrefBanLst = PrefBanLst
        self.DailyDict = DailyDict
        self.DailyChan = DailyChan
        self.EmoteNest = EmoteNest
        self.CommandPrefix = CommandPrefix
        self.PATH = PATH
        self.LogToFile = LogToFile
        self.AllowEmoji = AllowEmoji
        self.WeapList = WeapList
        self.DoLoadFile = DoLoadFile
        self.StephLog = StephLog
        for x in self.__TreeDir__:
            os.makedirs(os.path.join(self.PATH, x), exist_ok=True)
        if(DoLoadFile):
            try:
                self.load_from_file()
            except Exception:
                pass  # lol

    def __repr__(self):
        return(str(self.__dict__))

    def save_to_file(self):
        open(os.path.join(self.PATH, "Config.pkl"), "w").close()
        pickle.dump(self.__dict__, open(
            os.path.join(self.PATH, "Config.pkl"), "wb"))

    def load_from_file(self):
        'Like that one Matrix moive'
        new_self = pickle.load(
            open(os.path.join(self.PATH, "Config.pkl"), "rb"))
        self.TOKEN = new_self['TOKEN']
        self.DevLab = new_self['DevLab']
        self.LogChan = new_self['LogChan']
        self.LogAdmin = new_self['LogAdmin']
        self.SUPERUSER = new_self['SUPERUSER']
        self.UserExLixt = new_self['UserExLixt']
        self.ChanExList = new_self['ChanExList']
        self.GildExList = new_self['GildExList']
        self.WordExList = new_self['WordExList']
        self.WordBanLst = new_self['WordBanLst']
        self.PrefBanLst = new_self['PrefBanLst']
        self.DailyDict = new_self['DailyDict']
        self.DailyChan = new_self['DailyChan']
        self.EmoteNest = new_self['EmoteNest']
        self.CommandPrefix = new_self['CommandPrefix']
        self.PATH = new_self['PATH']
        self.LogToFile = new_self['LogToFile']
        self.AllowEmoji = new_self['AllowEmoji']
        self.WeapList = new_self['WeapList']
        self.DoLoadFile = new_self['DoLoadFile']
        self.StephLog = new_self['StephLog']
