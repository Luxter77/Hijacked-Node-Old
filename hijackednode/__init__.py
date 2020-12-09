from discord.ext.commands import Bot
from .configuration import CONF0
from .logger import LogMe
from .talk import TalkBox

config = CONF0()

talkbox = TalkBox(config=config)

bot = Bot(command_prefix=config.CommandPrefix, case_insensitive=True)

logMe = LogMe(config=config, bot=bot)
