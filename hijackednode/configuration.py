from base64 import standard_b64decode as de64
from discord import discord_Emoji
import random

# spoilers, its not funny
from hijackednode.funny import Pain

# Why do I keep doing this to myself
def saveConfig():
    try:
        pickle.dump(
            (
                CommandPrefix,
                TOKEN,
                PATH,
                DevLab,
                LogChan,
                LogAdmin,
                WeapList,
                SUPERUSER,
                UserExLixt,
                ChanExList,
                AllowEmoji,
                GildExList,
                WordExList,
                WordBanLst,
                DayList,
                DayChan,
                EmoteNest,
                StephLog,
            ),
            open("Config.pkl", "wb"),
        )
    except Exception:
        IAmIn = Pain(BaseException)  # Hug you Loop


def _get_def_doc() -> str:
    "Get Documents folder"
    if os.name == "nt":
        import ctypes.wintypes

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        return str(buf.value)
    else:
        import subprocess

        return subprocess.check_output(
            ["xdg-user-dir", "DOCUMENTS"], universal_newlines=True
        ).strip()


""" I'm unstoppable\n
I'm a Porsche with no brakes\n
I'm invincible\n
Yeah, I win every single game\n
I'm so powerful\n
I don't need batteries to play\n
I'm so confident, yeah, I'm unstoppable today\n
Unstoppable today, unstoppable today\n
Unstoppable today, yeah, I'm unstoppable today\n
Unstoppable today, unstoppable today\n
Unstoppable today, yeah, I'm unstoppable today\n"""

LogToFile = False
AllowEmoji = False

# Absolutely nessesary
CommandPrefix: str = "!"
TOKEN: str = ""
PATH: str = os.path.join(_get_def_doc(), "Hijacked-Node")
StephLog: str = ""

# Mix configs
DevLab: (list, str, set) = set()
LogChan: (list, str, set) = set()
LogAdmin: (list, str, set) = set()
SUPERUSER: (list, str, set) = set()
UserExLixt: (list, str, set) = set()
ChanExList: (list, str, set) = set()
GildExList: (list, str, set) = set()
WordExList: (list, str, set) = set()
WordBanLst: (list, str, set) = set()
DayList: (list, str, set) = set()
DayChan: (list, str, set) = set()
EmoteNest: (list, str, set) = set()

DayDict = {
    "We": os.path.join(PATH, "db", "img", "W.png"),
    "Th": os.path.join(PATH, "db", "img", "J.gif"),
    "Fr": os.path.join(PATH, "db", "img", "V.jpg"),
    "Sa": None,
    "Su": None,
    "Mo": None,
    "Tu": None,
}

WeapList = set(
    "Emojis",
    "Cringe",
    "A chainsaw",
    "Comnism",
    "Capitalism",
    "Anarchism",
    "Memes",
    "An informatic virus",
    "Yo' mama",
    "The BFG",
    "It's own guts",
    "My bare fists",
    "Extraneous furry imagery",
    "An orbital strike",
    "A rocket launcher",
    "A specially annoying kid with aspergers",
    "An assault rifle",
    "A Heaby machinegun",
    "It's own arms",
    "A nuclear bomb",
    "Puppies",
    "javascript",
    "Oracle®",
    "EvilCorp",
    "literally me",
    "A giantic book",
    "the power of God and anime",
)