from discord import TextChannel, User
from discord.ext.commands import Bot
from .configuration import CONF0
from tqdm.asyncio import tqdm
# class LogMe:
#     """This is a  complicated logger I came up with.\n
#     Feel free to insult me whilst readding it."""

#     _std = {
#         "LS": "|-----------------Log_ START-------------------|",
#         "ES": "|-----------------ERR_ START-------------------|",
#         "EE": "|------------------ERR_ END--------------------|",
#         "LE": "|------------------Log_ END--------------------|",
#         "!?": "Some unprintable error happened...",
#         "!!": "Ah for fucks sake something went horribly wrong!",
#     }

#     def __init__(self, bot: Bot, config: CONF0):
#         self.LogAdmin = set([bot.get_user(Admin) for Admin in config.LogAdmin])
#         self.LogChan = set([bot.get_channel(Chan) for Chan in config.LogChan])

#     async def __call__(self, st, err_: bool = False, tq: bool = True):
#         if err_:
#             print(self._std["ES"]) if (tq) else tqdm.write(self._std["ES"])
#             print(st) if (tq) else tqdm.write(st)
#             try:
#                 with self.bot.get_channel(self.LogChan) as chan:
#                     await chan.send()
#                     if self.LogAdmin:
#                         await chan.send(
#                             " ".join([str(admin.mention) for admin in self.LogAdmin])
#                         )
#                     await chan.send(st)
#                     await chan.send(self._std["EE"])
#             except Exception:
#                 try:
#                     with self.bot.get_channel(self.debug) as chan:
#                         await chan.send(self._std["ES"])
#                         try:
#                             if self.LogAdmin:
#                                 await chan.send(
#                                     " ".join(
#                                         [str(admin.mention) for admin in self.LogAdmin]
#                                     )
#                                 )
#                             await chan.send(str(st))
#                         except Exception:
#                             if self.LogAdmin:
#                                 await chan.send(
#                                     " ".join(
#                                         [str(admin.mention) for admin in self.LogAdmin]
#                                     )
#                                 )
#                             await chan.send("Some unprintable error happened...")
#                         await chan.send(self._std["EE"])
#                 except Exception:
#                     _std = "Ah for hugs sake something went horribly wrong! AGAIN"
#                     print(_std) if (tq) else tqdm.write(_std)
#             print(self._std["EE"]) if (tq) else tqdm.write(self._std["EE"])
#         else:
#             print(st) if (tq) else tqdm.write(st)
#             try:
#                 with self.bot.get_channel(self.debug) as chan:
#                     await chan.send(st)
#             except Exception:
#                 try:
#                     with self.bot.get_channel(self.debug) as chan:
#                         try:
#                             try:
#                                 await chan.send(st)
#                             except Exception:
#                                 await chan.send(str(type(st)))
#                                 await chan.send(str(st))
#                         except Exception:
#                             await chan.send(self._std["!?"])
#                 except Exception:
#                     await self(self._std["!!"], True)

#     def add_LogChan(self, Chan: TextChannel) -> None:
#         self.Logchan.add(Chan)

#     def del_LogChan(self, Chan: TextChannel) -> None:
#         self.Logchan.remove(Chan)

#     def add_LogAdmin(self, Admin: User) -> None:
#         self.LogAdmin.add(Admin)

#     def del_LogAdmin(self, Admin: User) -> None:
#         self.LogAdmin.remove(Admin)
