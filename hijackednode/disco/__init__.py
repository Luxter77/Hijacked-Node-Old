import asyncio

from typing import Union, Set, List

from discord.ext.commands import Bot
from discord import User, TextChannel, Guild

async def parse_channel_container(something: Union[str, int, TextChannel], bot: Bot) -> set:
    output = list()
    for thing in something:
        if(type(thing) is TextChannel):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            output.append(await bot.get_channel(thing))
        else:
            raise(TypeError(thing))
        return(set(output))

async def parse_user_container(something: Union[str, int, User], bot: Bot) -> set:
    output = list()
    for thing in something:
        if(type(thing) is User):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            output.append(await bot.get_user(thing))
        else:
            raise(TypeError(thing))
        return(set(output))

async def parse_guild_container(something: Union[str, int, Guild], bot: Bot) -> set:
    output = list()
    for thing in something:
        if(type(thing) is Guild):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            output.append(await bot.get_guild(thing))
        else:
            raise(TypeError(thing))
        return(set(output))
