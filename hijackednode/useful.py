import subprocess
import asyncio
import os

from typing import Union, Set, List
from random import randint

from discord.ext.commands import Bot
from discord import User, TextChannel, Guild


async def parse_channel_container(something: Union[str, int, TextChannel], bot: Bot) -> list:
    output = list()
    for thing in something:
        if(type(thing) is TextChannel):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            thing = bot.get_channel(thing)
            output.append(thing)
        else:
            raise(TypeError(thing))
    return(output)

async def parse_user_container(something: Union[str, int, User], bot: Bot) -> list:
    output = list()
    for thing in something:
        if(type(thing) is User):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            thing = bot.get_user(thing)
            output.append(thing)
        else:
            raise(TypeError(thing))
    return(output)

async def parse_guild_container(something: Union[str, int, Guild], bot: Bot) -> list:
    output = list()
    for thing in something:
        if(type(thing) is Guild):
            output.append(thing)
        elif((type(thing) is str) or (type(thing) is int)):
            thing = bot.get_guild(thing)
            output.append(thing)
        else:
            raise(TypeError(thing))
    return(output)

async def transsBack(cunn: str, b: bool = True) -> str:
    if(os.name == "nt"):
        return(cunn)  # windows bad linux good
    else:
        process = await asyncio.create_subprocess_exec(
            "apertium", ("en-es" if (b) else "es-en"), "-u",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=subprocess.PIPE,
        )   # fuck pythonic code, all my hommies hate pythonic code
            # - this post was made by the perl gang
        process.stdin.write(str(cunn).encode())
        conn, err_ = await process.communicate()
        if err_:
            raise(Exception(err_))
        conn = conn.decode("utf-8")
        await process.stdin.close()
        await process.terminate()
        return(conn)

def repl_fun() -> str:
    return str(randint(0, 9))
