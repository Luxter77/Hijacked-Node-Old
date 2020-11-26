import asyncio

from tqdm.asyncio import tqdm as asynctqdm
from tqdm.auto import tqdm

from discord.channel import TextChannel
from discord.ext.commands import Bot
from discord import User

from hijackednode.config import config

class LogMe:
    '''This is a  complicated logger I came up with.\n
    Feel free to insult me wilst readding it.'''

    _std = {'LS': '|-----------------Log_ START-------------------|',
            'ES': '|-----------------ERR_ START-------------------|',
            'EE': '|------------------ERR_ END--------------------|',
            'LE': '|------------------Log_ END--------------------|',
            '!?': "Some unprinteable error happened...",
            '!!': 'Ah for fucks sake something went horribly grong!'}

    def __init__(self, bot: Bot, config: CONF0):
        self.LogAdmin = set([bot.get_user(Admin) for Admin in config.LogAdmin])
        self.LogChan = set([bot.get_channel(Chan) for Chan in config.LogChan])

    async def __call__(self, st, err_: bool = False, tq: bool = True):
        if(err_):
            print(self._std['ES']) if (tq) else tqdm.write(self._std['ES'])
            print(st) if (tq) else tqdm.write(st)
            try:
                with self.bot.get_channel(self.LogChan) as Chan:
                    await Chan.send()
                    if (self.LogAdmin):
                        await Chan.send(
                            ' '.join([str(admin.mention) for admin in self.LogAdmin]))
                    await Chan.send(st)
                    await Chan.send(self._std['EE'])
            except:
                try:
                    with self.bot.get_channel(self.debug) as Chan:
                        await Chan.send(self._std['ES'])
                        try:
                            if (self.LogAdmin):
                                await Chan.send(
                                    ' '.join([str(admin.mention) for admin in self.LogAdmin]))
                            await Chan.send(str(st))
                        except:
                            if (self.LogAdmin):
                                await Chan.send(
                                    ' '.join([str(admin.mention)for admin in self.LogAdmin]))
                            await Chan.send("Some unprinteable error happened...")
                        await Chan.send(self._std['EE'])
                except:
                    _std = "Ah for hugs sake something went horribly grong! AGAIN"
                    print(_std) if (tq) else tqdm.write(_std)
            print(self._std['EE']) if (tq) else tqdm.write(self._std['EE'])
        else:
            print(st) if (tq) else tqdm.write(st)
            try:
                with self.bot.get_channel(self.debug) as Chan:
                    await Chan.send(st)
            except:
                try:
                    with self.bot.get_channel(self.debug) as Chan:
                        try:
                            try:
                                await Chan.send(st)
                            except:
                                await Chan.send(str(type(st)))
                                await Chan.send(str(st))
                        except:
                            await Chan.send(self._std['!?'])
                except:
                    await Chan.send(self._std['LS'])
                    await self(self._std['!!'], True)
                    await Chan.send(self._std['LE'])

    def add_LogChan(self, Chan: TextChannel) -> None:
        self.LogChan.add(Chan)

    def del_LogChan(self, Chan: TextChannel) -> None:
        self.LogChan.remove(Chan)

    def add_LogAdmin(self, Admin: User) -> None:
        self.LogAdmin.add(Admin)

    def del_LogAdmin(self, Admin: User) -> None:
        self.LogAdmin.remove(Admin)
