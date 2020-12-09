from typing import Union, Set, List

from tqdm.asyncio import tqdm

from discord import TextChannel, User
from discord.ext.commands import Bot

from .configuration import CONF0
from .useful import parse_channel_container, parse_user_container, parse_guild_container


class LogMe:
    """This is a  complicated logger I came up with.\n
    Feel free to insult me wilst readding it."""

    _std = {
        "LS": "|-----------------Log_ START-------------------|",
        "ES": "|-----------------ERR_ START-------------------|",
        "EE": "|------------------ERR_ END--------------------|",
        "LE": "|------------------Log_ END--------------------|",
        "!?": "Some unprinteable error happened...",
        "!!": "Ah for fucks sake something went horribly grong!",
    }

    def __init__(self, config: CONF0, bot: Bot):
        self.bot = bot
        self.config = config
        self.primed = False

    async def __call__(self, st, err_: bool = False, tq: bool = True):
        if err_:
            print(self._std["ES"]) if (tq) else tqdm.write(self._std["ES"])
            print(st) if (tq) else tqdm.write(st)
            if(self.primed):
                for chan in self.LogChan:
                    try:
                        if self.LogAdmin:
                            await chan.send(
                                " ".join([str(admin.mention)
                                        for admin in self.LogAdmin])
                            )
                        await chan.send(st)
                        await chan.send(self._std["EE"])
                    except Exception:
                        try:
                            await chan.send(self._std["ES"])
                            try:
                                if self.LogAdmin:
                                    await chan.send(
                                        " ".join(
                                            [str(admin.mention)
                                            for admin in self.LogAdmin]
                                        )
                                    )
                                await chan.send(str(st))
                            except Exception:
                                if self.LogAdmin:
                                    await chan.send(
                                        " ".join(
                                            [str(admin.mention)
                                            for admin in self.LogAdmin]
                                        )
                                    )
                                await chan.send("Some unprinteable error happened...")
                            await chan.send(self._std["EE"])
                        except Exception:
                            _std = "Ah for hugs sake something went horribly grong! AGAIN"
                            print(_std) if (tq) else tqdm.write(_std)
            print(self._std["EE"]) if (tq) else tqdm.write(self._std["EE"])
        else:
            print(st) if (tq) else tqdm.write(st)
            if(self.primed):
                for chan in self.LogChan:
                    try:
                        await chan.send(st)
                    except Exception:
                        try:
                            try:
                                try:
                                    await chan.send(st)
                                except Exception:
                                    await chan.send(str(type(st)))
                                    await chan.send(str(st))
                            except Exception:
                                await chan.send(self._std["!?"])
                        except Exception:
                            await chan.send(self._std["LS"])
                            await self(self._std["!!"], True)
                            await chan.send(self._std["LE"])

    def add_LogChan(self, chan: TextChannel) -> None:
        self.LogChan.add(chan)

    def del_LogChan(self, chan: TextChannel) -> None:
        self.LogChan.remove(chan)

    def add_LogAdmin(self, admin: User) -> None:
        self.LogAdmin.add(admin)

    def del_LogAdmin(self, admin: User) -> None:
        self.LogAdmin.remove(admin)
    
    def prime(self) -> None:
        self.LogAdmin = parse_user_container(
            something=self.config.LogAdmin, bot=self.bot)
        self.LogChan = parse_channel_container(
            something=self.config.LogChan, bot=self.bot)
        self.primed = True